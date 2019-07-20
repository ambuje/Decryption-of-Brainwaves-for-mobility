from pythonosc import dispatcher
from pythonosc import osc_server
import pandas as pd
from datetime import datetime
import time
import math
from keras.models import model_from_json
import json
import numpy as np

global dfList
global ip
global port

dfList = []
ip = "192.168.43.197"
port = 5006
evtcount=0
jawClench = 0
blinkToggle = 0

#JSON file
json_file = open('FBLR_HK_1_eegdata.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("HK_FBLR_model-170-0.818408-0.790441.h5")
loaded_model._make_predict_function()
print("Loaded model from disk")

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4, ch5):  
    global jawClench
    if jawClench % 2 != 0:
        return
    global evtcount
    evtcount += 1
    if evtcount % 500 != 0:
        return
    eegList = [ch1,ch2,ch3,ch4]
    eegList = np.array(eegList,'float64')
    eegList = eegList.reshape(1,4,1)
    prediction = loaded_model.predict(eegList)
    pred_a = prediction[0]
    pred_k = pred_a.max()
    #print("k ", k)
    list_q = list(pred_a)
    #print('qq ', qq)
    f = list_q.index(pred_k)
    #print('f ', f)
    if f==1:
        print("Forward")
        #client.publish(mqtt_topic1,"F")
    elif f==0:
        print("Backward")
        #client.publish(mqtt_topic1,"B")
    elif f==2:
        print("Left")
        #client.publish(mqtt_topic1,"L")
    elif f==3:
        print("Right")
        #client.publish(mqtt_topic1,"R")'''

def jaw_handler(unused_addr, args, blink):
    #print("blink", blink)
    global jawClench
    jawClench += 1
    
def blink_handler(unused_addr, args, jaw):
    #print("jaw", jaw)
    global jawClench
    if jawClench % 2 != 0:
        return
    global blinkToggle
    blinkToggle += 1
    
dispatcher = dispatcher.Dispatcher()

dispatcher.map("/muse/elements/blink", blink_handler, "Blink")
dispatcher.map("/muse/elements/jaw_clench", jaw_handler, "Jaw")
dispatcher.map("/muse/eeg",eeg_handler,"EEG")

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Serving on {}".format(server.server_address))

while True:
    server.handle_request()
