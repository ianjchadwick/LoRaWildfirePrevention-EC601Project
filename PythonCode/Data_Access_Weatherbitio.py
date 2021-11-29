#!/usr/bin/env python
import requests
import json

class Wind:

    def __init__(self, *args):
        # Three ways option: By GPS, By City name, By PostCode
        self.API_key = '476a2c1d68b847a0988d42e9eeab46c3'
        self.key = 0
        if args[0] == 'ByGPS':
            self.lat = args[1]
            self.lon = args[2]
            self.startDate = args[3]
            self.endDate = args[4]
            self.key = 1
        elif args[0] == 'ByCity':
            self.city = args[1]
            self.startDate = args[3]
            self.endDate = args[4]
            self.key = 2
        elif args[0] == 'ByPostCode':
            self.post_code = args[1]
            self.country = args[2]
            self.startDate = args[3]
            self.endDate = args[4]
            self.key = 3
        else:
            return

    def __repr__(self):
        return 'Object: {}'.format(self.Wind)

    def request_by_GPS(self):
        base_url = f"https://api.weatherbit.io/v2.0/history/subhourly?" \
                   f"lat={self.lat}&lon={self.lon}" \
                   f"&start_date={self.startDate}&end_date={self.endDate}" \
                   f"&tz=local&key={self.API_key}"
        r = requests.get(base_url)
        data_daily = json.loads(r.text)
        return data_daily

    def main(self):
        attributes = {}
        if self.key == 1:
            json_data = self.request_by_GPS()
            data_of_weather = json_data['data']
            # Obtain the value of Sub_Data for a specific day for the nodes
            wind_direction = {}
            wind_speed = {}
            frequent = 0
            for sub_data in data_of_weather:
                # We could also tried for the same way to access for different kinds of species based on the API support,
                # For here I just took the wind_speed and direction which we most need in time.
                # Documentation for sub-hourly(15 minutes period): https://www.weatherbit.io/api/weather-history-daily
                time_stamp = sub_data['timestamp_local']
                wind_speed[time_stamp] = sub_data['wind_spd']
                wind_direction[time_stamp] = sub_data['wind_dir']
                if frequent == 0:
                    attributes = sub_data.keys()
                    frequent = 1

        for key in wind_speed:
            print(f"Wind_Speed: {wind_speed[key]}, Direction: {wind_direction[key]}, at time: {key}, ")

        # List of the species of data
        print(attributes)

if __name__ == '__main__':
    # Now it is the version based on accurate GPS, they another two ways which is by City and by PostCode,
    # If we need, I could expand my code in order to get through data by those options.
    get_wind_GPS = Wind('ByGPS', '42.350097', '-71.156442', '2021-11-20', '2021-11-21')
    get_wind_GPS.main()
