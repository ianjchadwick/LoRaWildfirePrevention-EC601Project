#!/usr/bin/env python
import requests
import json

X_AIO_Key = "aio_bspQ29zZjgMMQgEhUKISmDWA9IgF"
feed_key = "lora-wildfire-nodes"
user_name = "IanJChadwick"

class DataTransmission:

    def __init__(self, *args):
        self.x_aio_key = args[0]
        self.user_name = args[1]
        self.feed_key = args[2]

    def request_adafruit(self):
        # get the most recent value
        base_url = f"https://io.adafruit.com/api/v2/{self.user_name}" \
                   f"/groups/{self.feed_key}?x-aio-key={self.x_aio_key}"
        try:
            r = requests.get(base_url)
            data_sensor = json.loads(r.text)
            last_value = data_sensor['feeds']
            return last_value

        except requests.exceptions.RequestException as e:
            print(e)
            raise SystemExit(e)

    def dealwith_data(self):
        sensorData = self.request_adafruit()
        latest_value = {}
        for data in sensorData:
            latest_value[data['name']] = [data['last_value'], data['created_at']]
            print(latest_value[data['name']])

        return latest_value

# test for running:
if __name__ == '__main__':
    # Arguments requirement:
    #   First: X_AIO_Key for adafruit gateway
    #   Second： UserName of the adafruit gateway
    #   Third: Current Feed-Key for adafruit gateway
    # Etc:
    #   X_AIO_Key = "aio_bspQ29zZjgMMQgEhUKISmDWA9IgF"
    #   user_name = "IanJChadwick"
    #   feed_key = "lora-wildfire-nodes"

    test = DataTransmission(X_AIO_Key, user_name, feed_key)
    test.dealwith_data()