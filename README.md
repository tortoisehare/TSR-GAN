# TSR-GAN
1) Data
2) Dataset Creation and Preprocessing
3) Classifier Models

1. Data:
Our data came from the German Traffic Sign Dataset (pickled files found here: https://d17h27t6h515a5.cloudfront.net/topher/2017/February/5898cd6f_traffic-signs-data/traffic-signs-data.zip)

This dataset contains 50,000+ images in 43 classes and was used for our Traffic Sign Recognition (TSR) classifier as well as our combined TSR+CIFAR10 classifier. We used CIFAR10 images as a "not a sign" class for some of our models: https://www.cs.toronto.edu/~kriz/cifar.html

Class Breakdown in TSR Datasets:

Training set is: (36699, 32,32,3) + labels column

![Alt text](images/train.png?raw=true "Training Set Class Breakdown")


Test set is: (13313, 32,32,3) + labels column

![Alt text](images/test.png?raw=true "Test Set Class Breakdown")


Validation set is: (4645, 32,32,3) + labels column

![Alt text](images/valid.png?raw=true "Validation Set Class Breakdown")

2. Dataset Creation and Preprocessing
TSRGAN_dataprep.ipynb contains code which pulls the German Traffic sign images as well as random CIFAR10 images, putting the CIFAR10 images under one class label.  We first tried to create a model that would overfit and learn on a small, 3-class dataset containing two signs and the "not a sign" class.  This code generated numpy arrays for the 3-class dataset as well as the "all-class" datasets.

Preprocessing steps taken:
*shuffle
*grayscale

These steps are found in the classifier codes.

3. Classifier Models

3-Class Models:
We also tried a general fully connected neural network on the 3-class dataset. FC_NN_classifier.py refers to the fully connected (FC) neural network (NN) which was developed to classify between 3 classes (2 traffic signs + a "not-a-sign" class consisting of various CIFAR images). tf_utils.py contains the mini batch generator and conver-to-one-hot functions used in FC_NN_classifier.py.

TSR Models:
