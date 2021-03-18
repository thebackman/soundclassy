""" this runs on zero and listens """


# code from
# https://tutorials-raspberrypi.de/datenaustausch-raspberry-pi-mqtt-broker-client/

	
import os
import paho.mqtt.client as mqtt
 
MQTT_SERVER = "localhost"
MQTT_PATH = "recording_channel"
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # more callbacks, etc
    os.system('sudo python3 /home/pi/Projects/TheHat/heartbeat.py 2 reds')
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
