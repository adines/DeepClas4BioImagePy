from imagepy.core.engine import Free
from imagepy import IPy
import platform
import subprocess
import json
import wx
from imagepy.ui.panelconfig import ParaDialog
from imagepy.core.util import fileio
import os
from wx import DirPickerCtrl


class Plugin(Free):
    title = 'DeepClas4BioPy'
    model = ''
    framework = ''
    python = ''
    pathAPI = ''

    def load(self):

        dirdialog=wx.DirDialog(IPy.get_window(),message=wx.DirSelectorPromptStr, defaultPath="",
          style=wx.DD_DEFAULT_STYLE, pos=wx.DefaultPosition, size=wx.DefaultSize,
          name=wx.DirDialogNameStr)

        if dirdialog.ShowModal() == wx.ID_OK:
            self.pathAPI = dirdialog.GetPath()
            self.pathAPI=self.pathAPI+os.path.sep
        else:
            return False

        if platform.system() == 'Windows':
            self.python = 'python'
        else:
            self.python = 'python3'
        subprocess.check_output([self.python, self.pathAPI + 'listFrameworks.py'])
        data = json.load(open('data.json'))
        frameworks = data['frameworks']

        subprocess.check_output([self.python, self.pathAPI + 'listModels.py', '-f', 'Keras'])
        data = json.load(open('data.json'))
        models = data['models']

        Para = {'f': 'Keras', 'm': 'VGG16'}
        View = [('lab', 'Select the framework and the model'),
                (list, frameworks, str, 'Framework', 'f', ''),
                (list, models, str, 'Model', 'm', '')
                ]
        md = MyDialog(None, 'DeepClas4BioPy', self.pathAPI, self.python, View, Para)
        md.initView()

        if md.ShowModal() == wx.ID_OK:
            self.framework = md.para['f']
            self.model = md.para['m']
            md.Destroy()
            return True
        else:
            md.Destroy()
            return False

    def run(self, para=None):
        imp = IPy.get_ips()
        if imp is None:
            IPy.alert("Please open the image you want to classify", 'Error')
            return
        name = imp.title
        recent = fileio.recent
        for i in recent:
            pos1 = i.rfind(os.sep)
            pos2 = i.rfind('.')
            if name == i[pos1 + 1:pos2]:
                image = i

        subprocess.check_output(
            [self.python, self.pathAPI + 'predict.py', '-i', image, '-f', self.framework, '-m', self.model])
        data = json.load(open('data.json'))
        className = data['class']
        IPy.alert("The class which the image belongs is " + className, 'Prediction')


class MyDialog(ParaDialog):
    pathAPI = ''
    python = ''

    def __init__(self, parent, title, pathApi, python, view, para):
        ParaDialog.__init__(self, parent, title)
        self.para = para
        self.view = view
        self.pathAPI = pathApi
        self.python = python

    def para_changed(self, key):
        ParaDialog.para_changed(self, key)
        if key == 'f':
            subprocess.check_output([self.python, self.pathAPI + 'listFrameworks.py'])
            data = json.load(open('data.json'))
            frameworks = data['frameworks']
            framework = self.para[key]
            subprocess.check_output([self.python, self.pathAPI + 'listModels.py', '-f', framework])

            data = json.load(open('data.json'))
            models = data['models']
            self.para = {'f': framework, 'm': models[0]}
            self.view = [('lab', 'Select the framework and the model'),
                         (list, frameworks, str, 'Framework', 'f', ''),
                         (list, models, str, 'Model', 'm', '')
                         ]
            for child in self.GetChildren():
                child.Destroy()
            self.tus = []
            self.initView()
            self.Layout()

    def initView(self):
        ParaDialog.init_view(self, self.view, self.para)


class OpenPathAPI(fileio.Reader):
    title = "Select the path of the API"
    filt = ["dir"]
