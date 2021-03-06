# -*- coding: utf-8 -*-
"""target_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nRmuQwv5JZWdKcZe_rvoOC2-ZMYI4xFt
"""

'''
Defines a target classifier with 94.4% validation accuracy, 92.1% test accuracy on the German TSR dataset


'''

import numpy as np
np.random.seed(1187) #to help reproduce

#from __future__ import print_function
import tensorflow as tf
import matplotlib.pyplot as plt
import os
import csv
#import random
#import cv2
#from skimage.filters import rank
#import skimage.morphology as morp
from sklearn.metrics import confusion_matrix
from sklearn.utils import shuffle

#from keras.utils import to_categorical
#from keras.models import Sequential
from keras.layers import Flatten
#from keras.layers import Convolution2D, MaxPooling2D
from keras import optimizers



class Target:
    def __init__(self, lr=0.001, epochs=15, n_input=32, n_classes=43, batch_size=20, restore=0):
        self.lr = lr
        self.epochs = epochs
        self.n_input = 32
        self.n_classes = 43
        self.batch_size = batch_size
        self.restore = restore

        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    
    '''
    def next_batch(self, X, Y, i, batch_size):
      idx = i*batch_size
      idx_n = idx + batch_size
      return X[idx:idx_n], Y[idx:idx_n]
      '''
    
    def Model(self, x):
        with tf.variable_scope('Model', reuse=tf.AUTO_REUSE):
            # Hyperparameters
            mu = 0
            sigma = 0.1
            n_out = self.n_classes
            learning_rate = self.lr

            # Layer 1 (Convolutional): Input = 32x32x1. Output = 28x28x6.
            filter1_width = 5
            filter1_height = 5
            input1_channels = 1
            conv1_output = 6
            # Weight and bias
            conv1_weight = tf.Variable(tf.truncated_normal(
                shape=(filter1_width, filter1_height, input1_channels, conv1_output),
                mean = mu, stddev = sigma))
            conv1_bias = tf.Variable(tf.zeros(conv1_output))

            # Apply Convolution
            conv1 = tf.nn.conv2d(x, conv1_weight, strides=[1, 1, 1, 1], padding='VALID') + conv1_bias

            # Activation:
            conv1 = tf.nn.relu(conv1)

            # Pooling: Input = 28x28x6. Output = 14x14x6.
            conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

            # Layer 2 (Convolutional): Output = 10x10x16.
            filter2_width = 5
            filter2_height = 5
            input2_channels = 6
            conv2_output = 16
            # Weight and bias
            conv2_weight = tf.Variable(tf.truncated_normal(
                shape=(filter2_width, filter2_height, input2_channels, conv2_output),
                mean = mu, stddev = sigma))
            conv2_bias = tf.Variable(tf.zeros(conv2_output))

            # Apply Convolution
            conv2 = tf.nn.conv2d(conv1, conv2_weight, strides=[1, 1, 1, 1], padding='VALID') + conv2_bias

            # Activation:
            conv2 = tf.nn.relu(conv2)

            # Pooling: Input = 10x10x16. Output = 5x5x16.
            conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

            # Flattening: Input = 5x5x16. Output = 400.
            fully_connected0 = Flatten()(conv2)

            # Layer 3 (Fully Connected): Input = 400. Output = 120.
            connected1_weights = tf.Variable(tf.truncated_normal(shape=(400, 120), mean = mu, stddev = sigma))
            connected1_bias = tf.Variable(tf.zeros(120))
            fully_connected1 = tf.add((tf.matmul(fully_connected0, connected1_weights)), connected1_bias)

            # Activation:
            fully_connected1 = tf.nn.relu(fully_connected1)

            # Layer 4 (Fully Connected): Input = 120. Output = 84.
            connected2_weights = tf.Variable(tf.truncated_normal(shape=(120, 84), mean = mu, stddev = sigma))
            connected2_bias = tf.Variable(tf.zeros(84))
            fully_connected2 = tf.add((tf.matmul(fully_connected1, connected2_weights)), connected2_bias)

            # Activation.
            fully_connected2 = tf.nn.relu(fully_connected2)
    
            # Layer 5 (Fully Connected): Input = 84. Output = 43.
            output_weights = tf.Variable(tf.truncated_normal(shape=(84, 43), mean = mu, stddev = sigma))
            output_bias = tf.Variable(tf.zeros(43))
            logits =  tf.add((tf.matmul(fully_connected2, output_weights)), output_bias)


            return logits
    
    
    
    def test(self, X_data, BATCH_SIZE=64):
        num_examples = len(X_data)
        y_pred = np.zeros(num_examples, dtype=np.int32)
        sess = tf.get_default_session()
        for offset in range(0, num_examples, BATCH_SIZE):
            batch_x = X_data[offset:offset+BATCH_SIZE]
            y_pred[offset:offset+BATCH_SIZE] = sess.run(tf.argmax(logits, 1), 
                               feed_dict={x:batch_x, keep_prob:1, keep_prob_conv:1})
        return y_pred
    
    
    def train(self, X_train, Y_train, X_valid, Y_valid):
        #placeholders for inputs
        x = tf.placeholder(tf.float32, (None, 32, 32, 1))
        y = tf.placeholder(tf.int32, (None))

        keep_prob = tf.placeholder(tf.float32)       # For fully-connected layers
        keep_prob_conv = tf.placeholder(tf.float32)

        #define graph
        logits = self.Model(x)
        
              # Training operation
        one_hot_y = tf.one_hot(y, 43)
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits, labels=one_hot_y)
        loss_operation = tf.reduce_mean(cross_entropy)
        optimizer = tf.train.AdamOptimizer(learning_rate = self.lr)
        training_operation = optimizer.minimize(loss_operation)

        # Accuracy operation
        correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(one_hot_y, 1))
        accuracy_operation = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


          # Saving all variables
        saver = tf.train.Saver()

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            num_train = len(Y_train)
            num_valid = len(Y_valid)
            print("Training ...")
            print()
            EPOCHS = self.epochs
            BATCH_SIZE = self.batch_size
            DIR = "./weights/target_model"
            total_batch = int(X_train.shape[0] / self.batch_size)

            for i in range(EPOCHS):
                avg_cost = 0.
                total_accuracy = 0
                validation_accuracy = 0
                #Train set
                for offset in range(0, num_train, BATCH_SIZE):
                    end = offset + BATCH_SIZE
                    batch_x, batch_y = X_train[offset:end], Y_train[offset:end]
                    _, c = sess.run([training_operation, loss_operation], feed_dict={x: batch_x, y: batch_y, keep_prob : 0.6, keep_prob_conv: 0.8})
                    avg_cost += c / total_batch
                    
                    #Validation Set
                for offset in range(0, num_valid, BATCH_SIZE):
                    end = offset + BATCH_SIZE
                    batch_x, batch_y = X_valid[offset:end], Y_valid[offset:end]
                    accuracy = sess.run(accuracy_operation, 
                                    feed_dict={x: batch_x, y: batch_y, keep_prob: 1.0, keep_prob_conv: 1.0 })
                    total_accuracy += (accuracy * len(batch_x))
                    validation_accuracy = total_accuracy / num_valid
                    #print("Validation Accuracy = {:.3f}%".format(validation_accuracy*100))
                    
                print("Epoch: ", '%04d' % (i+1), "cost=", "{:.9f}".format(avg_cost))
                print("EPOCH {} : Validation Accuracy = {:.3f}%".format(i+1, (validation_accuracy*100)))
            
            
            #Test set
            num_examples = len(X_test)
            y_pred = np.zeros(num_examples, dtype=np.int32)
            #sess = tf.get_default_session()
            for offset in range(0, num_examples, BATCH_SIZE):
                batch_x = X_test[offset:offset+BATCH_SIZE]
                y_pred[offset:offset+BATCH_SIZE] = sess.run(tf.argmax(logits, 1), 
                                   feed_dict={x:batch_x, keep_prob:1, keep_prob_conv:1})
            test_accuracy = sum(Y_test == y_pred)/len(Y_test)
            print("Test Accuracy = {:.1f}%".format(test_accuracy*100))

            cm = confusion_matrix(Y_test, y_pred)
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            cm = np.log(.0001 + cm)
            plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
            plt.title('Log of normalized Confusion Matrix')
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            plt.show()
            
            saver.save(sess, "./weights/target_model/model.ckpt")
            print("Model saved")
            sess.close()

   
      
      
import pickle

if __name__ == '__main__':
    training_file = 'train.p'
    testing_file = 'test.p'
    validation_file = 'valid.p'

    with open(training_file, mode='rb') as f:
        tstrain = pickle.load(f)
    with open(testing_file, mode='rb') as f:
        tstest = pickle.load(f)
    with open(validation_file, mode='rb') as f:
        tsvalid = pickle.load(f)

    X_train, Y_train = tstrain['features'], tstrain['labels']
    X_valid, Y_valid = tsvalid['features'], tsvalid['labels']
    X_test, Y_test = tstest['features'], tstest['labels']

    #shuffle training set
    X_train, Y_train = shuffle(X_train, Y_train)

    #grayscale images
    grayscale = [0.299,0.587,0.144]

    X_test = np.dot(X_test, grayscale)
    X_train = np.dot(X_train, grayscale)
    X_valid = np.dot(X_valid, grayscale)


    #normalize
    X_train = np.array(X_train)/255
    X_test = np.array(X_test)/255
    X_valid = np.array(X_valid)/255

    #expand dimensions to fit 4D input array
    X_train = np.expand_dims(X_train,-1)
    X_test = np.expand_dims(X_test,-1)
    X_valid = np.expand_dims(X_valid,-1)

    assert(len(X_train)==len(Y_train))
    n_train = len(X_train)
    assert(len(X_test)==len(Y_test))
    n_test = len(X_test)

    cnn = Target()
    cnn.train(X_train, Y_train, X_valid, Y_valid)
