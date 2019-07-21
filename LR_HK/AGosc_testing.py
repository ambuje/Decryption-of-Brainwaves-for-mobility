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

#Location Of JSON file
json_file = open('LR_HK_1_eegdata.json', 'r')
#json_file = open('pkmkb(70).json', 'r')

loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
# Write the file name of the weights
#loaded_model.load_weights("pkmkb(70)_weights.h5")
loaded_model.load_weights("HK_LR_model-188-0.744898-0.787879.h5")
loaded_model._make_predict_function()
print("Loaded model from disk")

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4, ch5):
  
    global evtcount
    evtcount +=1
    if evtcount %500 !=0:
        return
  #print(args[0], ch1, " - ",ch2, " - ",ch3, " - ",ch4)
  #l = [ch1,ch2,ch3,ch4]
  #dfList.append(l)
  #print(dfList)
    y=[ch1,ch2,ch3,ch4]
    y=np.array(y,'float64')
    y=y.reshape(1,4,1)
  #print("@@@@@@@@@@")
    prediction = loaded_model.predict(y)
  #print("********")
  #print(prediction)
    aa=prediction[0]
    k=aa.max()
  #print("k ", k)
    qq=list(aa)
  #print('qq ', qq)
    f=qq.index(k)
  #print('f ', f)
    #if f==1:
     #   print("Forward")
     # client.publish(mqtt_topic1,"F")
   # elif f==0:
    #    print("Backward")
   #   client.publish(mqtt_topic1,"B")
    if f==0:
        print("Left")
     # client.publish(mqtt_topic1,"L")
    elif f==1:
        print("Right")
    #  client.publish(mqtt_topic1,"R")'''
  
'''def delta_handler(unused_addr, args, c1,c2,c3,c4,c5):
  print(args[0],' - ',c1)'''

dispatcher = dispatcher.Dispatcher()

dispatcher.map("/muse/eeg",eeg_handler,"EEG")

#dispatcher.map("/muse/elements/delta_absolute",delta_handler,"delta")
#dispatcher.map("/muse/elements/theta_absolute",print)
#dispatcher.map("/muse/elements/alpha_absolute",print)
#dispatcher.map("/muse/elements/beta_absolute",print)
#dispatcher.map("/muse/elements/gamma_absolute",print)
#dispatcher.map("/muse/eeg",print)

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Serving on {}".format(server.server_address))

'''def disp():
  server.handle_request()'''
    
if __name__ == "__main__":
  while True:
    #disp()
    server.handle_request()
    #time.sleep(1)
