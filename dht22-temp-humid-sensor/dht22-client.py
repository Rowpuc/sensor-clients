#!/usr/bin/python
import Adafruit_DHT as dht
import time
import json
import paho.mqtt.client as paho
broker="192.168.1.250"
client = paho.Client("dht22-client")

print("Connecting to Broker",broker)
try:
  client.connect(broker)
except:
  print"Connect to Client Failed"

#Uses Read Retry to pull data on GPIO 4 pin
DATAPIN = 17 #gpio pin that dht22 sensor is on

while True:
  try:
    h,t = dht.read_retry(dht.DHT22, DATAPIN)        #get the temp and humid data fr$
    print ('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(t, h))
    
    temperaturePacket = {
    "type": "Temperature",
    "value": round(t,2),
    "sensorId": "Temp-001",
    "uploaded": False
    }
    humidityPacket = {
    "type": "Humidity",
    "value" : round(h,2),
    "sensorId": "Humid-001",
    "uploaded": False
    }
    temperatureJsonPacket = json.dumps(temperaturePacket)
    humidityJsonPacket = json.dumps(humidityPacket)
    
    client.loop_start()
    print("Publishing")
    client.publish("/test/topic", temperatureJsonPacket)
    client.publish("/test/topic", humidityJsonPacket)
    time.sleep(10)
  
  except:
    pass
  
client.disconnect()
client.loop_stop()


