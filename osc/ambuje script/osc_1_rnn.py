import argparse

import math
import time
from keras.models import model_from_json
import json
import numpy as np

import time
#Location Of JSON file
json_file = open('bot.json', 'r')
#json_file = open('pkmkb(70).json', 'r')

loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
# Write the file name of the weights
#loaded_model.load_weights("pkmkb(70)_weights.h5")
loaded_model.load_weights("model-250-0.798153-0.802632.h5")
loaded_model._make_predict_function()
print("Loaded model from disk")


from pythonosc import dispatcher

from pythonosc import osc_server
'''
TP9, AF7, AF8, TP10'''

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4,ch5):
    #print("ch1",ch1,'\n')
    
    print('yes')
    y=[ch1,ch2,ch3,ch4]
    
    y=np.array(y,'float64')
    y=y.reshape(1,4,1)
    print("@@@@@@@@@@")
    prediction = loaded_model.predict(y)
    print("********")
    #print(prediction)
    aa=prediction[0]
    k=aa.max()
    #print("k ", k)
    qq=list(aa)
    #print('qq ', qq)
    f=qq.index(k)
    #print('f ', f)
    if f==0:
        print("Forward")
       # client.publish(mqtt_topic1,"F")
    elif f==1:
        print("Backward")
     #   client.publish(mqtt_topic1,"B")
    elif f==2:
        print("Left")
       # client.publish(mqtt_topic1,"L")
    elif f==3:
        print("Right")
      #  client.publish(mqtt_topic1,"R")'''
    
    



ip = "192.168.0.124"
port = 5005


dispatcher = dispatcher.Dispatcher()

dispatcher.map("/muse/eeg", eeg_handler, "EEG")

server = osc_server.ThreadingOSCUDPServer(
    (ip, port), dispatcher)

# print("Serving on {}".format(server.server_address))
server.serve_forever()





