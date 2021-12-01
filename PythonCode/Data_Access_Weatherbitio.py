#!/usr/bin/env python
import requests
import json
import grab_from_Adafruit

# Enter the API key of Weatherbitio at here:

API_key = '476a2c1d68b847a0988d42e9eeab46c3'

class Weatherbitio:

    def __init__(self, *args):
        # Three ways option: By GPS, By City name, By PostCode
        self.API_key = API_key
        self.API_atributes = []
        self.mode = 0
        if args[0] == 'ByGPS':
            self.lat = args[1]
            self.lon = args[2]
            self.startDate = args[3]
            self.endDate = args[4]
            self.pattern = args[5]
            self.mode = 1
        elif args[0] == 'ByCity':
            self.city = args[1]
            self.startDate = args[2]
            self.endDate = args[3]
            self.pattern = args[4]
            self.mode = 2
        elif args[0] == 'ByPostCode':
            self.post_code = args[1]
            self.country = args[2]
            self.startDate = args[3]
            self.endDate = args[4]
            self.pattern = args[5]
            self.mode = 3
        else:
            return

    def __repr__(self):
        return 'Object: {}'.format(self.Wind)

    def request_by_GPS(self):
        try:
            base_url = f"https://api.weatherbit.io/v2.0/history/{self.pattern}?" \
                       f"lat={self.lat}&lon={self.lon}" \
                       f"&start_date={self.startDate}&end_date={self.endDate}" \
                       f"&tz=local&key={self.API_key}"
            r = requests.get(base_url)
            data_daily = json.loads(r.text)
            return data_daily

        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)

    def access_data(self):
        if self.mode == 1:
            json_data = self.request_by_GPS()
            data_of_weather = json_data['data']
            # Obtain the value of Sub_Data for a specific day for the nodes
            frequent = 0
            for sub_data in data_of_weather:
                if frequent == 0:
                    for attributes in sub_data.keys():
                        self.API_atributes.append(attributes)
                    frequent = 1

        return data_of_weather

    # We could also tried for the same way to access for different kinds of species based on the API support,
    # For here I just took the wind_speed and direction which we most need in time.
    # Documentation for sub-hourly(15 minutes period): https://www.weatherbit.io/api/weather-history-daily

    def get_precipitation_data(self):
        data_weatherbit = self.access_data()
        precipitation = {}
        precipitation_rate = {}
        for sub_data in data_weatherbit:
            time_stamp = sub_data['timestamp_local']
            if self.pattern == 'subhourly':
                precipitation_rate[time_stamp] = sub_data['precip_rate']
            else:
                precipitation[time_stamp] = sub_data['precip']

        if self.pattern == 'subhourly':
            return precipitation_rate
        else:
            return precipitation


    def get_wind_data(self):
        data_weatherbit = self.access_data()
        wind_data = {}
        for sub_data in data_weatherbit:
            time_stamp = sub_data['timestamp_local']
            wind_data[time_stamp] = [sub_data['wind_spd'], sub_data['wind_dir']]

        return wind_data


# Test Main Function:
if __name__ == '__main__':
    # Access the 12000 meteorological stations data by specify the "START" and the "END" of day with an accurate GPS, City or PostCode,
    # Note: If you want to access the most recently data (Subhourly and Hourly mode only);
    #       Define the interval between most current until the next available day of the current:
    #       Example: Most Current time: 12/01/2021, You should specify the interval start with: 12/01/2021, end with: 12/02/2021
    test = Weatherbitio('ByGPS', '42.350097', '-71.156442', '2021-12-01', '2021-12-02', 'subhourly')
    wind = test.get_wind_data()
    precipitation = test.get_precipitation_data()

    # Test access the data subhourly by the time_stamp:
    for key in wind:
        print(f"Precipitation rate: {precipitation[key]}, Wind_Speed: {wind[key][0]}, Direction: {wind[key][1]}, at time: {key}, ")
