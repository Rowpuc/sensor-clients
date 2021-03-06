#!/usr/bin/python
 
import spidev
import time
import os
import json
import paho.mqtt.client as paho

broker="192.168.1.250"
client = paho.Client("ldr-client")

print("Connecting to Broker",broker)
try:
  client.connect(broker)
except:
  print"Connect to Client Failed"
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
 
# Define sensor channels
light_channel = 2
 
# Define delay between readings
delay = 5
 
while True:
 
  # Read the light sensor data
  light_level = ReadChannel(light_channel)
  light_volts = ConvertVolts(light_level,2)
 
  # Print out results
  print "--------------------------------------------"
  print("Light: {} ({}V)".format(light_level,light_volts))
  
  try:    
    lightPacket = {
      "type": "Light",
      "value": light_level,
      "sensorId": "LDR-Light",
      "uploaded": False
    }
    lightJsonPacket = json.dumps(lightPacket)
    
    client.loop_start()
    print("Publishing")
    client.publish("/test/topic", lightJsonPacket)
    time.sleep(3)
  except:
    pass

client.disconnect()
client.loop_stop()
