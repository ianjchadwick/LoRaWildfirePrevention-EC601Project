"""
This script runs on the LoRa gateway and receives timestamped temperature and humidity data from the nodes, decodes it
and uploads it to cloud service dashboard.

Code specific to the Adafruit RFM95W LoRa Radio Bonnet adapted from:
Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x

# Converts a bytearray packet input back to a list of floats or integers in the format
# [nodeID, temp, humidity, year, month, day, hours, minutes, seconds]
def packet_decode(byte_array):
    inc_str = str(byte_array, "utf-8")
    temp_str = ""
    packet_list = []
    for element in inc_str:
        if element != " ":
            temp_str = temp_str + element
        elif element == " ":
            if '.' in temp_str:
                value = float(temp_str)
            else:
                value = int(temp_str)
            temp_str = ""
            packet_list.append(value)
    return packet_list

if __name__ == '__main__':

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

    while True:
        packet = None
        # draw a box to clear the image
        display.fill(0)
        display.text('RasPi LoRa', 35, 0, 1)

        # check for packet rx
        packet = rfm9x.receive()
        if packet is None:
            display.show()
            display.text('- Waiting for PKT -', 15, 20, 1)
        else:
            packet_received = packet_decode(packet)
            print(packet_received)

        time.sleep(0.1)