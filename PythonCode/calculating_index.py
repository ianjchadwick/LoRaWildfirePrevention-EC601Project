import math
import grab_from_Adafruit as Grab_Adafruit
import fire_weather_index_class as FWI_Calculation
import Data_Access_Weatherbitio as Weather_Access

X_AIO_Key = ""
user_name = ""
feed_key = ""


class Vapor_Pressure_Deficit:
	def __init__(self, *args):
		print("init function")

class Calculate_Index:
	def __init__(self, *args):
		self.getWeather = Weather_Access
		self.getNode = Grab_Adafruit.DataTransmission(X_AIO_Key, user_name, feed_key)
		self.getFwi = FWI_Calculation.Fire_Weather_Index()
		self.gps = args[0] 		   	# Dictionary of GPS of nodes
		self.fwi_initial = args[1]	# FWI index boolean
		print(f"Calculate FWI Index:(Updating at 12:00PM on each day), "
			  f"and Vapor Pressure Deficit (Updating with real-time Node data)")

	def calculate(self) -> dict():
		node_information = self.getNode.dealwith_data()
		# If the feeds never update node's fwi value before:
		current_Nodehum = 0
		current_Nodetemp = -375
		fwi_input = {}
		for key_node in list(node_information):
			'''
			Note: Please use specific name to give the name of feeds of Fire Wire Index and the relevant values of each node,
			which instead of start with "Node # ...". Otherwide the code won't work !!
			'''

			# Feeds which not start with "Node 2, 3 ...": Not humidity or tempreture data:
			if "Node" not in key_node:
				break
			node_name = str(key_node)[5:6]
			data_type = str(key_node)[7::]
			# Get Most current Relative-Humidity data from the sensor node
			if str(data_type) == "Humidity":
				current_Nodehum = float(node_information.get(key_node)[0])
			# Get Most current Tempreture data from the sensor node
			elif str(data_type) == "Temperature":
				current_Nodetemp = float(node_information.get(key_node)[0])

			# Get Most current Timestamp from the sensor node
			current_node_time = node_information.get(key_node)[1]

			if current_Nodetemp > -375 and current_Nodehum > 0:
				current_node_gps = str()
				# Pair a GPS Location by the input of the current node:
				for key_gps in self.gps.keys():
					if node_name == key_gps:
						# Get accurate GPS for the current sensor node
						current_node_gps = self.gps.get(key_gps)

				# Get accurate local time for the sensor node
				time_In_Date = current_node_time.split("T")[0]
				time_In_Hours = current_node_time.split("T")[1]
				# Check Adafruit Cloud, if time is at the noon: 12PM.
				# If it is, then calculate the current FWI Scale value of the previous day:
				if int(time_In_Hours[0:2]) > 12:
					current_month = int()
					total_precip = float()
					avg_wind = float()
					current_month = int(time_In_Date[5:7])
					date = int(time_In_Date[8::])
					start_date = time_In_Date[0:7] + '-' + str(int(date)-1)
					end_date = time_In_Date[0:7] + '-' + str(int(date)+1)
					Weather = self.getWeather.Weatherbitio('By History', current_node_gps[0], current_node_gps[1],
														   start_date, end_date, 'hourly')
					weather_data = Weather.get_average()
					total_precip = weather_data[0]
					avg_wind = weather_data[1]
					# Use the sensor data from the current node, and also weather station, calculate its FWI relavant value,
					# Then, store it as a dictionary which corresponds with each node:
					fwi_input[str(key_node)[5:6]] = [current_Nodetemp, current_Nodehum, current_month, avg_wind, total_precip]

				current_Nodehum = 0
				current_Nodetemp = -375

		if self.fwi_initial == True:
			# For each node: Calculate its FFMC, DMC, DC and FWI scalar value
			node_update = {}
			for node_key in list(fwi_input):
				node = fwi_input.get(node_key)
				ffmc = self.getFwi.fine_fuel_moisture_code(node[0], node[1], node[3], node[4])
				dmc = self.getFwi.duff_moisture_code(node[1], node[0], node[4], node[2])
				dc = self.getFwi.drought_code(node[0], node[4], node[2])
				fwi_scalar = self.getFwi.fire_weather_index(node[0], node[1], node[2], node[3], node[4])
				print(ffmc, dmc, dc, fwi_scalar)
				node_update[node_key] = [ffmc, dmc, dc, fwi_scalar]

			return node_update

		'''
		If the feeds has the fwi value of each node: bring the value into the calculation
		'''
		# else:




""" Test for running: """

if __name__ == '__main__':

	node_gps = {'1': [39.588394, -122.871460], '2': [39.588066, -122.831039], '3': [39.603593, -122.864541], '4': [39.603359, -122.830615]}
	recent_Feeds = Grab_Adafruit.DataTransmission(X_AIO_Key, user_name, feed_key).dealwith_data()
	for feeds_data in recent_Feeds:
		if "FWI" in feeds_data:
			fwi_initial = False
		else:
			fwi_initial = True

	a = Calculate_Index(node_gps, fwi_initial)
	a.calculate()