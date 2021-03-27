""" this sends a message """

import paho.mqtt.publish as publish
 
MQTT_SERVER = "192.168.2.115"
MQTT_PATH = "recording_channel"
 
publish.single(MQTT_PATH, "Hello World!", hostname=MQTT_SERVER)

