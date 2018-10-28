#!/usr/bin/python
import time
import json
import paho.mqtt.client as paho
import RPi.GPIO as GPIO

broker="192.168.1.250"
client = paho.Client("pir-client")

print("Connecting to Broker",broker)
try:
  client.connect(broker)
except:
  print("Connect to Client Failed")

DATAPIN = 7 #gpio pin that motion sensor is on
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATAPIN, GPIO.IN)
 
def motion_callback(channel):
  # Here, alternatively, an application / command etc. can be started.
  print('Movement Detected')
  try:
    motionpacket = {
      "type": "Motion",
      "value": 1,
      "sensorId": "Pir-Motion",
      "uploaded": False
    }
    motionpacket = json.dumps(motionpacket)
    
    time.sleep(5)
  except:
    pass
  
  client.loop_start()
  print("Publishing")
  client.publish("/test/topic", motionpacket)
  client.disconnect()
 
try:
    GPIO.add_event_detect(DATAPIN, GPIO.RISING, callback=motion_callback)
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print "Finish..."
GPIO.cleanup()

