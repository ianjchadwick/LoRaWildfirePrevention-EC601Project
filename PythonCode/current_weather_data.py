#!/usr/bin/env python
import requests
import json
import os
import Data_Access_Weatherbitio.py

key = os.getenv("WEATHERBIT_API_KEY")


# Calls to current weather API returns the most recent reading from the nearest weather station to a given GPS location


def weather_data_request(lat, lon, API_key):
    base_url = f"https://api.weatherbit.io/v2.0/current?" \
                f"lat={lat}&lon={lon}" \
                f"&key={API_key}"
    r = requests.get(base_url)
    data = json.loads(r.text)
    return data

# Extract wind data from API json
def get_fwi_data(data):
    wind = data.get('data')[0].get('wind_spd')
    precipitation = data.get('data')[0].get('precip')
    return [wind, precipitation]


if __name__ == '__main__':
    # Now it is the version based on accurate GPS, they another two ways which is by City and by PostCode,
    # If we need, I could expand my code in order to get through data by those options.
    lat = 42.350097
    lon = -71.156442
    tempKey = "insert API key"
    data = weather_data_request(lat, lon, tempKey)
