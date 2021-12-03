#!/usr/bin/env python
import requests
import time
import json
import grab_from_Adafruit

# Enter the API key of Weatherbitio at here:

API_key = ''

class Weatherbitio:

    def __init__(self, *args):

        """
            Option:  By GPS
            Four Patterns:  Historical:     Daily, Hourly, Subhourly; 
                            Current:        Minutely
            Same way to access for different kinds of species based on the API support
            Documentation for sub-hourly(15 minutes period): https://www.weatherbit.io/api/weather-history-daily
        """ 

        self.API_key = API_key
        self.API_atributes = []
        self.mode = 0
        if args[0] == 'By History':
            self.lat = args[1]
            self.lon = args[2]
            self.startDate = args[3]
            self.endDate = args[4]
            self.pattern = args[5]
            self.mode = 1
        elif args[0] == 'By Current':
            self.lat = args[1]
            self.lon = args[2]
            # self.pattern = args[3]
            self.mode = 2
        else:
            return

    def __repr__(self):
        return 'Object: {}'.format(self.Wind)

    def request_by_GPS(self):
        if self.mode == 1:
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


    def request_by_GPS_current(self):
        if self.mode == 2:
            try:
                base_url = f"https://api.weatherbit.io/v2.0/current?" \
                           f"lat={self.lat}&lon={self.lon}" \
                           f"&key={self.API_key}&include=minutely"
                r = requests.get(base_url)
                data_minute = json.loads(r.text)
                return data_minute

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

        elif self.mode == 2:
            json_current = self.request_by_GPS_current()
            data_current = json_current['data']
            data_current_list = []
            for c_data in data_current:
                data_current_list.append(c_data['wind_spd'])
                data_current_list.append(c_data['ob_time'])
                data_current_list.append(c_data['timezone'])

            return data_current_list

            # return data_minutely


    def get_historical_data(self) -> dict:
        data_weatherbit = self.access_data()
        historical_data = {}
        last_precipitation = float()
        precipitation_sum = 0.0
        for sub_data in data_weatherbit:
            time_stamp = sub_data['timestamp_local']
            if sub_data['wind_spd'] is None:
                break

            if self.pattern == 'subhourly':
                historical_data[time_stamp] = [float(sub_data['precip_rate']), float(sub_data['wind_spd']), float(sub_data['wind_dir'])]
            else:
                historical_data[time_stamp] = [float(sub_data['precip']), float(sub_data['wind_spd']), float(sub_data['wind_dir'])]

        return historical_data

    def get_average(self) -> list:

        if self.pattern == 'hourly':
            historical_data = self.get_historical_data()
            precipitation_sum = 0.0
            wind_sum = 0.0
            for key in historical_data:
                precipitation_sum = historical_data[key][0] + precipitation_sum
                wind_sum = historical_data[key][1] + wind_sum

            avg_windspeed = float(wind_sum / len(historical_data))
            avg_prepitation = float(precipitation_sum / len(historical_data))

            return [avg_prepitation, avg_windspeed]

        else:
            return None
"""

Access the 12000 meteorological stations data by specify the "START" and the "END" of day with an accurate GPS, City or PostCode.

Note: If you want to access the most recently data (Subhourly and Hourly mode only);  
    Define the interval between most current to the next available day of the current:
    Example: Most Current time: 12/01/2021, You should specify the interval start with: 12/01/2021, 
    end with: 12/02/2021
"""

# Test Main Function:
if __name__ == '__main__':
    
    test = Weatherbitio('By History', '42.350097', '-71.156442', '2021-12-03', '2021-12-04', 'hourly')
    hist = test.get_historical_data()
    average = test.get_average()
    # Test access the data subhourly by the time_stamp:
    for key in hist:
        print(f"Precipitation: {hist[key][0]}, Wind_Speed: {hist[key][1]}, Direction: {hist[key][2]}, at time: {key}, ")
    print(f"Average precipitation: {average[0]}, wind speed: {average[1]}")
    # test2 = Weatherbitio('By Current', '42.350097', '-71.156442')
    # data = test2.access_data()
    # print(f"Last Observation Wind speed: {data[0]}, Time: {data[1]}, Zone: {data[2]}")



