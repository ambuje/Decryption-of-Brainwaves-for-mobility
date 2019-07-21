import paho.mqtt.client as mqtt

mqtt_username = "username"
mqtt_password = "qwertyuiop"
#mqtt_topic = "test1"
mqtt_topic = "runbot"
mqtt_broker_ip = "10.16.1.36"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print ("Connected!", str(rc))
    
client.on_connect = on_connect
client.connect(mqtt_broker_ip, 1883)
while True:
  client.publish("test","ek")
