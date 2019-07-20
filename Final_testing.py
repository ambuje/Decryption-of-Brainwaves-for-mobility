from pythonosc import dispatcher
from pythonosc import osc_server
import pandas as pd
import time
import math
from keras.models import model_from_json
import json
import numpy as np
import paho.mqtt.client as mqtt

mqtt_username = "username"
mqtt_password = "qwertyuiop"
mqtt_topic = "runbot"
mqtt_topic1 = "jawClench"
mqtt_topic2 = "blink"
mqtt_topic3 = "eeg"
mqtt_topic4 = "head"
mqtt_topic5 = "pred"
mqtt_topic6 = "horseshoe"
mqtt_topic7 = "fit"
mqtt_broker_ip = "10.16.1.36"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print ("Connected!", str(rc))
client.on_connect = on_connect
client.connect(mqtt_broker_ip, 1883)

global dfList
global ip
global port
global predList
global FB
global LR

predList = []
dfList = []
ip = "192.168.43.197"
port = 5006
evtcount=0
jawClench = 0
blinkToggle = 0

#JSON file FB
json_file = open('FBLR_HK_1_eegdata.json', 'r')
loaded_model_json_fb = json_file.read()
json_file.close()
loaded_model_fb = model_from_json(loaded_model_json_fb)
# load weights into new model
loaded_model_fb.load_weights("HK_FBLR_model-170-0.818408-0.790441.h5")
loaded_model_fb._make_predict_function()
print("Loaded FB model from disk")

#JSON file LR
json_file = open('FBLR_HK_1_eegdata.json', 'r')
loaded_model_json_lr = json_file.read()
json_file.close()
loaded_model_lr = model_from_json(loaded_model_json_lr)
# load weights into new model
loaded_model_lr.load_weights("HK_FBLR_model-170-0.818408-0.790441.h5")
loaded_model_lr._make_predict_function()
print("Loaded LR model from disk")

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4, ch5):  
    global jawClench
    if jawClench % 2 != 0:
        return
    global evtcount
    evtcount += 1
    if evtcount % 500 != 0:
        return
    eegList = [ch1,ch2,ch3,ch4]
    client.publish(mqtt_topic3, eegList)
    eegList = np.array(eegList,'float64')
    eegList = eegList.reshape(1,4,1)
    global LR
    global FB
    if LR == 0 and FB == 1:
        prediction = loaded_model_fb.predict(eegList)
    elif FB == 0 and LR == 1:
        prediction = loaded_model_lr.predict(eegList)
    pred_a = prediction[0]
    pred_k = pred_a.max()
    #print("k ", k)
    list_q = list(pred_a)
    #print('qq ', qq)
    f = list_q.index(pred_k)
    #print('f ', f)
    global predList
    if f==0:
        predList.append(0)
    elif f==1:
        predList.append(1)
    if len(predList) >= 10:
        fPred = max(set(predList), key = predList.count) 
        if LR == 0 and FB == 1:
            if fPred == 0:
                print("Forward")
                client.publish(mqtt_topic,"F")
                client.publish(mqtt_topic5,"F")
            elif fPred == 1:
                print("Backward")
                client.publish(mqtt_topic,"B")
                client.publish(mqtt_topic5,"B")
        elif FB == 0 and LR == 1:
            if fPred == 0:
                print("Left")
                client.publish(mqtt_topic,"L")
                client.publish(mqtt_topic5,"L")
            elif fPred == 1:
                print("Right")
                client.publish(mqtt_topic,"R")
                client.publish(mqtt_topic5,"R")

def jaw_handler(unused_addr, args, blink):
    #print("blink", blink)
    global jawClench
    jawClench += 1
    print("Jaw Clench")
    client.publish(mqtt_topic1, "Jaw Clench")
    
def blink_handler(unused_addr, args, jaw):
    global jawClench
    if jawClench % 2 != 0:
        return
    global blinkToggle
    global LR
    global FB
    blinkToggle += 1
    print("Blink")
    if blinkToggle % 2 == 0:
        LR = 1
        FB = 0
        print("LR")
    else:
        LR = 0
        FB = 1
        print("FB")
    client.publish(mqtt_topic2, "Blink")

def head_handler(unused_addr, args, x, y, z):
    xyz = [x,y,z]
    print("xyz", xyz)
    client.publish(mqtt_topic4, str(xyz))

def horseshoe_handler(unused_addr, args,c1,c2,c3,c4):
    c1234 = [c1,c2,c3,c4]
    print("c1234",c1234)
    client.publish(mqtt_topic6, str(c1234))

def fit_handler(unused_addr, args, fit):
    print("Fit", fit)
    client.publish(mqtt_topic7, fit)
    
dispatcher = dispatcher.Dispatcher()

dispatcher.map("/muse/elements/blink", blink_handler, "Blink")
dispatcher.map("/muse/elements/jaw_clench", jaw_handler, "Jaw")
dispatcher.map("/muse/eeg", eeg_handler, "EEG")
dispatcher.map("/muse/gyro", head_handler, "Head")
dispatcher.map("/muse/elements/horseshoe",horseshoe_handler,"HorseShoe")
dispatcher.map("/muse/elements/touching_forehead",fit_handler,"Fit")

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Serving on {}".format(server.server_address))

while True:
    server.handle_request()
