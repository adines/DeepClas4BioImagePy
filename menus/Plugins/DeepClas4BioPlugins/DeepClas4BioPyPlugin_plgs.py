from imagepy.core.engine import Free
from imagepy import IPy
import wx
from imagepy.ui.panelconfig import ParaDialog
from imagepy.core.util import fileio
import os
import deepclas4bio as dc4b


class Plugin(Free):
    title = 'DeepClas4BioPy'
    model = ''
    framework = ''

    def load(self):
        frameworks = dc4b.listFrameworks()
        models = dc4b.listModels('Keras')

        Para = {'f': 'Keras', 'm': 'VGG16'}
        View = [('lab','lab', 'Select the framework and the model'),
                (list, 'f', frameworks, str, 'Framework', ''),
                (list, 'm', models, str, 'Model', '')
                ]
        md = MyDialog(None, 'DeepClas4BioPy',View, Para)
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

        className = dc4b.predict(image,self.framework,self.model)
        IPy.alert("The class which the image belongs is " + className, 'Prediction')


class MyDialog(ParaDialog):
    pathAPI = ''
    python = ''

    def __init__(self, parent, title,view, para):
        ParaDialog.__init__(self, parent, title)
        self.para = para
        self.view = view

    def para_changed(self, key):
        ParaDialog.para_changed(self, key)
        if key == 'f':
            frameworks = dc4b.listFrameworks()
            framework = self.para[key]
            models = dc4b.listModels(framework)
            self.para = {'f': framework, 'm': models[0]}
            self.view = [('lab', 'lab','Select the framework and the model'),
                         (list, 'f', frameworks, str, 'Framework',  ''),
                         (list,'m', models, str, 'Model',  '')
                         ]
            for child in self.GetChildren():
                child.Destroy()
            self.tus = []
            self.initView()
            self.Layout()

    def initView(self):
        ParaDialog.init_view(self, self.view, self.para)

