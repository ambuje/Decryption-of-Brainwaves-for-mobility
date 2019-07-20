from pythonosc import dispatcher
from pythonosc import osc_server
import pandas as pd
from datetime import datetime
import time

global dfList
global ip
global port

dfList = []
ip = "192.168.43.68"
port = 5006

evtcount = 0

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4, ch5):
  global evtcount
  evtcount += 1
  if evtcount % 50 != 0:
    return
  #print(ch1)
  print(args[0], ch1, " - ",ch2, " - ",ch3, " - ",ch4)
  l = [ch1,ch2,ch3,ch4]
  dfList.append(l)

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

startTime = time.time()

while True:
  server.handle_request()
  if (time.time()) - startTime >= 60:
    break
      
df = pd.DataFrame(dfList, columns =['ch1', 'ch2', 'ch3', 'ch4'])
print(df)
df.to_csv('R_AG_11_eegdata.csv' ,index=False)
