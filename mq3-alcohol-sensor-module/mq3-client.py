#!/usr/bin/python
from mq import *
import sys, time
import json
import paho.mqtt.client as paho

mq = MQ();
broker="192.168.1.250"
client = paho.Client("mq3-client")

print("Connecting to Broker",broker)
try:
  client.connect(broker)
except:
  print"Connect to Client Failed"

while True:
  try:
    perc = mq.MQPercentage()
    print("\033[K")
    print("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
     
    lpgPacket = {
      "type": "LPG",
      "value": perc["GAS_LPG"],
      "sensorId": "MQ3-LPG",
      "uploaded": False
    }
    coPacket = {
      "type": "CO",
      "value" : perc["CO"],
      "sensorId": "MQ3-CO",
  	  "uploaded": False
    }
    smokePacket = {
      "type": "Smoke",
      "value" : perc["SMOKE"],
      "sensorId": "MQ3-Smoke",
      "uploaded": False
    }
    lpgJsonPacket = json.dumps(lpgPacket)
    coJsonPacket = json.dumps(coPacket)
    smokeJsonPacket = json.dumps(smokePacket)
    
    client.loop_start()
    print("Publishing")
    client.publish("/test/topic", lpgJsonPacket)
    client.publish("/test/topic", coJsonPacket)
    client.publish("/test/topic", smokeJsonPacket)
    time.sleep(10)
  except:
    pass

client.disconnect()
client.loop_stop()
