#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 22:58:54 2019

@author: ambuje
"""


#L=0

import numpy as np

import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense

from keras.layers import Dropout , Flatten

from sklearn import preprocessing
#Give the pathof the file
data=pd.read_csv('FB_HKAG_11_eegdata.csv',encoding='utf-8')

#data=pd.read_csv('training',delimiter='\t',encoding='utf-8')
x_data=data.iloc[:,0:4]
y_data=data.iloc[:, 4]
y=np.array(x_data,'float64')
#Pre-Processing of data

labelencoder = LabelEncoder()
y_data[:] = labelencoder.fit_transform(y_data[:])

from keras.utils import to_categorical
y_data=to_categorical(y_data)
#Splitting into train-test
X_train, X_test, Y_train, Y_test = train_test_split(x_data, y_data, test_size=0.25)
print('x_train shape:',X_train.shape)
print('x_test shape:', X_test.shape)
print('Y_train shape:', Y_train.shape)
print('Y_test shape:', Y_test.shape)


X_train=X_train.values.reshape(915,4,1)
X_test=X_test.values.reshape(305,4,1)



from keras import regularizers

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers.normalization import BatchNormalization
# Initialising the RNN
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.regularizers import l2
from keras import optimizers
checkpoint = ModelCheckpoint('FB_HKAG_11_eegdata_model-{epoch:03d}-{acc:03f}-{val_acc:03f}.h5', verbose=2, monitor='val_acc',save_best_only=True, mode='auto')
model_classifier = Sequential()
model_classifier.add(LSTM(128, return_sequences = True, input_shape = (X_train.shape[1], 1)))
model_classifier.add(BatchNormalization())

model_classifier.add(LSTM(128, return_sequences = True,activation='relu',bias_regularizer=l2(0.01)))
Dropout(0.2)
model_classifier.add(BatchNormalization())
model_classifier.add(LSTM(128, return_sequences = True,activation='tanh',bias_regularizer=l2(0.01)))
Dropout(0.2)
model_classifier.add(BatchNormalization())
model_classifier.add(LSTM(128,return_sequences = True, activation='relu',bias_regularizer=l2(0.01)))
Dropout(0.2)
model_classifier.add(BatchNormalization())
'''model_classifier.add(LSTM(25,return_sequences = True, activation='relu',bias_regularizer=l2(0.01)))

model_classifier.add(BatchNormalization())
model_classifier.add(LSTM(25,return_sequences = True, activation='relu',bias_regularizer=l2(0.01)))
Dropout(0.2)
model_classifier.add(BatchNormalization())
model_classifier.add(LSTM(25,return_sequences = True, activation='relu',bias_regularizer=l2(0.01)))
Dropout(0.2)
model_classifier.add(BatchNormalization())
model_classifier.add(LSTM(25,return_sequences = True, activation='relu',bias_regularizer=l2(0.01)))'''

model_classifier.add(LSTM(64, activation='relu',bias_regularizer=l2(0.001)))
model_classifier.add(BatchNormalization())
#model_classifier.add(Dense(1, activation='sigmoid'))
model_classifier.add(Dense(2, activation='softmax',kernel_regularizer=regularizers.l2(0.001)))


model_classifier.summary()

# Compiling the RNN
opt=optimizers.Adam(lr=0.0009, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.01, amsgrad=False)
model_classifier.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
#callbacks = [EarlyStopping(monitor='val_loss', patience=7)]
# Fitting the RNN to the Training set
model_classifier.fit(X_train, Y_train, 
          batch_size=64, 
          epochs=500, 
          callbacks=[checkpoint],
          validation_data=(X_test, Y_test),shuffle='false')



score, acc = model_classifier.evaluate(X_test, Y_test, batch_size=128)
print('Test score:', score)
print('Test accuracy:', acc)

model_json = model_classifier.to_json()

# Write the file name of the model

with open("FB_HKAG_11_eegdata.json", "w") as json_file:
    json_file.write(model_json)
    
# serialize weights to HDF5
# Write the file name of the weights
model_classifier.save_weights("FB_AGHK.h5")
print("Saved model to disk")



