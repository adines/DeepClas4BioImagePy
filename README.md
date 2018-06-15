# DeepClas4BioPy

DeepClas4BioPy is an ImagePy plugin that connects ImagePy with the [DeepClas4Bio API](https://github.com/adines/DeepClas4Bio).  This plugin allows ImagePy users to use deep learning techniques for object classification abstracting deep learning techniques details. 

## Requirements
To use this plugin is necessary to have installed ImagePy with python 3.6 and download the [DeepClas4Bio API](https://github.com/adines/DeepClas4Bio).

## Installation
To install this plugin you have to download it and put it in the path imagepy --> menus --> Plugins --> DeepClas4Bio.

## Using the plugin
In this section, we will see an example of how to use this plugin. For this example we will classify a lion image using the VGG16 model from the Keras framework. In addition, you can use the model and the framework that best suits to your problem. 

To use the plugin you must follow the following steps:

 1. Load the image that you want to classify
![Loading the image](docs/images/001.png)


 2. Run the plugin
 
 Go to Plugins and search the name of the plugin in this case DeepClas4BioPy.

 
 3. Indicate the path to DeepClas4Bio API
 
![Path of the API](docs/images/002.png)


 4. Select the framework and the model you want use
 ![Select framework and model](docs/images/003.png)

 
 5. Visualize the output
 ![Visualize the output](docs/images/004.png)
