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

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4, ch5):
  print(args[0], ch1, " - ",ch2, " - ",ch3, " - ",ch4)
  l = [ch1,ch2,ch3,ch4]
  dfList.append(l)
  #print(dfList)
  
def delta_handler(unused_addr, args, c1,c2,c3,c4,c5):
  print(args[0],' - ',c1)

def head_handler(unused_addr, args, x, y, z):
  print(args,x,y,z)
  
dispatcher = dispatcher.Dispatcher()

dispatcher.map("/muse/gyro", head_handler, "Head")
dispatcher.map("/muse/eeg",eeg_handler,"EEG")

#dispatcher.map("/muse/elements/delta_absolute",delta_handler,"delta")
#dispatcher.map("/muse/elements/theta_absolute",print)
#dispatcher.map("/muse/elements/alpha_absolute",print)
#dispatcher.map("/muse/elements/beta_absolute",print)
#dispatcher.map("/muse/elements/gamma_absolute",print)
#dispatcher.map("/muse/eeg",print)

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Serving on {}".format(server.server_address))

def disp():
  server.handle_request()
    
if __name__ == "__main__":
  c=120
  while (c>0):
    disp()
    time.sleep(1)
    c=c-1
        
  '''df = pd.DataFrame(dfList, columns =['ch1', 'ch2', 'ch3', 'ch4'])
  print(df)
  df.to_csv('B_AG_eegdata.csv' ,index=False)
  
  dateTime = str(datetime.now())
  fileName = ('eegdata' + dateTime + '.csv').strip()
  df.to_csv(fileName ,index=False)'''
