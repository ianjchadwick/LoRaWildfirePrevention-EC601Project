"""
This script runs on the LoRa nodes. It reads the temperature and humidity data from the AM2302 sensors and transmits
the timestamped temperature and humidity data on the LoRa 915Hz band every 5 seconds.

Code specific to the Adafruit RFM95W LoRa Radio Bonnet adapted from:
Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import os to handle requests for env variables
import os
# Import libraries for AM2302 Sensor
import Adafruit_DHT
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x


# Takes sensor data and packages it with timestamp for transmission. Packet format is a byte array
#  with space separated values: nodeID, temp, humidity, year, month, day, hours, minutes, seconds, ssk
def packet_encode(temperature, humidity, node_id, ssk):
    timestamp = time.localtime()
    temperature = round(temperature, 2)
    humidity = round(humidity, 2)
    pack_list = [node_id, temperature, humidity, timestamp[0], timestamp[1], timestamp[2], timestamp[3], timestamp[4], timestamp[5], ssk]
    pack_str = ' '.join(map(str,pack_list)) + " "
    packet = bytes(pack_str, "utf-8")
    return packet


# Declare DHT sensor constant
DHT_SENSOR = Adafruit_DHT.AM2302

# Define data pin input
DHT_PIN = 4

# Get node ID number from env
NODE_ID = os.getenv("NODE_ID")

# Get ID key to include in packet to ensure the receiving gateway only adds data meant for our network to the cloud
SSK = int(os.getenv("SSK"))

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None
state=0

# Loops indefinitely transmitting a packet with temperature, humidity, node coordinates, and time every 30 minutes
#get current time
transmit_interval = 5
now = time.monotonic()
while True:

    if not btnA.value:
        # Press Button A
        # Ready state
        state=0

    elif not btnB.value:
        # Press Button B
        #Single transmit
        state=1

    elif not btnC.value:
        # Press Button C
        #Continuous transmit
        state=2
    else:
        state=state
    
    if state ==0:
        #display Ready state
        display.fill(0)
        display.text('Ready state', 10, 15, 1)
        display.show()
    elif state ==1:
        #revert state back to ready state
        state =0
        # Get sensor data and put it into timestamped bytearray packet
        humidityRead, temperatureRead = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidityRead is not None and temperatureRead is not None:
            data_packet = packet_encode(temperatureRead, humidityRead, NODE_ID, SSK)
            display.fill(0)
            display.text('Single Temp={0:0.1f}*C  Hum={1:0.1f}%'.format(temperatureRead, humidityRead), 10, 15, 1)
        else:
            display.fill(0)
            display.text('Failed to retrieve data', 25, 15, 1)  
        
        # Send packet
        rfm9x.send(data_packet)
            
        display.show()
        
        #sleep for 1 second to act as debouncing and prevent duplicate transmission
        time.sleep(1)
        
    elif state ==2:
        #Take action if the transmit interval has elapsed
        if time.monotonic() - now > transmit_interval:
            now = time.monotonic()
            
            # Get sensor data and put it into timestamped bytearray packet
            humidityRead, temperatureRead = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if humidityRead is not None and temperatureRead is not None:
                data_packet = packet_encode(temperatureRead, humidityRead, NODE_ID, SSK)
                display.fill(0)
                display.text('Sent Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperatureRead, humidityRead), 25, 15, 1)
            else:
                display.fill(0)
                display.text('Failed to retrieve data', 25, 15, 1)

            # Send packet
            rfm9x.send(data_packet)
            
            display.show()
            
            
            
        
