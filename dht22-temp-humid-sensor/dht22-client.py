#!/usr/bin/python
import Adafruit_DHT as dht
import time
import json
import paho.mqtt.client as paho
broker="192.168.1.250"
client = paho.Client("client-001")
#Uses Read Retry to pull data on GPIO 4 pin
DATAPIN = 17 #gpio pin that dht22 sensor is on
h,t = dht.read_retry(dht.DHT22, DATAPIN)        #get the temp and humid data fr$
print ('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(t, h))
try:
	temppacket = {
                "type": "Temperature",
                "value": t,
                "sensorId": "Temp-001",
		"uploaded": False
        }
        humidpacket = {
                "type": "Humidity",
                "value" : h,
                "sensorId": "Humid-001",
		"uploaded": False
        }
        humidjsonpacket = json.dumps(humidpacket)
        tempjsonpacket = json.dumps(temppacket)

#        print(tempjsonpacket)
#        print(humidjsonpacket)

except:
        pass

	print("Connecting to Broker",broker)
try:
        client.connect(broker)
except:
        print"Connect to Client Failed"

client.loop_start()
print("Publishing")
while True:
	client.publish("/test/topic", tempjsonpacket)
	client.publish("/test/topic", humidjsonpacket)
	#print "loop"
	time.sleep(1)

client.disconnect()
client.loop_stop()

