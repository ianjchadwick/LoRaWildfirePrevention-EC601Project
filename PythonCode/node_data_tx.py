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
SSK = os.getenv("SUPER_SECRET_KEY")

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None


if __name__ == '__main__':

    # Loops indefinitely transmitting a packet with temperature, humidity, node coordinates, and time every 5 seconds
    while True:
        # Get sensor data and put it into timestamped bytearray packet
        humidityRead, temperatureRead = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidityRead is not None and temperatureRead is not None:
            data_packet = packet_encode(humidityRead, temperatureRead, NODE_ID, SSK)
        else:
            print("Failed to retrieve data from humidity sensor")

        # Send packet
        rfm9x.send(data_packet)

        time.sleep(5)
