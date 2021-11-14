import Adafruit_DHT
import time

# Declare DHT sensor constant
DHT_SENSOR = Adafruit_DHT.AM2302

# Define data pin input
DHT_PIN = 4

# Loops indefinitely
while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from sensor")
    time.sleep(3)
