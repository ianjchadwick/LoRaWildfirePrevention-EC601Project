# LoRa Wildfire Prevention Project - EC601

## Goal
Our objective is to build a proof-of-concept IoT system of low-power, low-cost sensor nodes which measure temperature and relative humidity data, and use this data to refine remote sensing data in order to improve the accuracy of existing wildfire prediction models. Our hope is that more data will allow decision makers and stakeholders, such as firefighting organizations and local government officials to allocate resources more efficiently, in hopes of preventing catastrophic wildfire losses. See the [original proposal in the wiki](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Project-Proposal) for more details.

### Project Management Methods
* The project was implemented using the AGILE framework (see the [project page](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/projects/1) for kanban board) over the course of five two-week sprints.

## Hardware and Software Set-Up
### Sensor Node Hardware
We utilized RaspberryPi Zero based sensor nodes with a LoRa radio transciever module and an AM2302 sensor to record temperature and relative humidity data, and transmit it via LoRa on the ISM 915MHz band to a central gateway every 60 minutes.
* We used a [RaspberryPI Zero](https://www.adafruit.com/product/3708) with headers installed as the base for the other breakouts.
* A [LoRa radio transceiver module](https://www.adafruit.com/product/4074) was added to the Pi via the headers.
* An [AM2302 temperature and humidity sensor](https://www.adafruit.com/product/393) was soldered to GPIO pin 4, the 5V, and GND on the LoRa tansceiver module.
* An on/off switch, and the USB-A jack was was soldered to the [PowerBoost chip](https://www.adafruit.com/product/1903) (see [this link](https://learn.adafruit.com/adafruit-powerboost-500-plus-charger/on-slash-off-switch) for specifics)]
* The [900MHz antenna](https://www.adafruit.com/product/3340) was attached to the uFL port on the LoRa module
* A 2000mAh 3.7V LiPo battery was connected to the PowerBoost chip via the JST connector and the USB-A jack was connected to the Pi Zero's power-in USB-B port.
### Gateway Hardware
The gateway receives and decodes the data from the nodes, performs the calculations to determine the meterics for Fire Weather Index (and the components FFMC, DMC and DC), Vapor Pressure Deficit (VPD), and uploads the data to Adafruit.io.
* We used a [Rasberry Pi 3 B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/) as the base for the breakouts to build the gateway.
* Similarly to the nodes, a [LoRa radio transceiver module](https://www.adafruit.com/product/4074) was added to the Pi 3 via the headers.
* Again, the [900MHz antenna](https://www.adafruit.com/product/3340) was attached to the uFL port on the LoRa module.
* The Pi was connected to power via a USB-B 5V wall outlet.

### General Software Set-Up
The nodes and gateways are running the Raspbian operating system with the CircuitPython libraries for the firmware for the LoRa radio module and AM2302 sensors.
* [RasbianOS](https://www.raspberrypi.com/software/) was installed on an 8GB SD card for the nodes and a 32GB SD card for the gateway.
* CircuitPython was installed on the gateway and each of the nodes following the [outline provided here](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi).
* Then the radio modules were set-up by installing the necessary modules [discussed here](https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi/rfm9x-raspberry-pi-setup).
* The DHT22 sensor module was insalled utilizing [the adafruit circuit python libraries](https://learn.adafruit.com/dht/dht-circuitpython-code)
### Node-specific Software Set-up
* The nodes each have environments variable set for: 
>* NODE_ID="unique integer" this ID identifies the node so that its location and data values can be determined by the gateway
>* SSK="Integer Key" this acts as a key to ensure that the data received by the gateway is data sent by a node on the LoRa network, and not some different LoRa transmission that happened to be on the same 915MHz band.
* The nodes then have [node_data_tx.py from PythonCode](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/blob/main/PythonCode/node_data_tx.py) in the same directory as the set-up files for CircuitPython (and font5x8.bin file required for the OLED).
### Gateway-specific Software Set-up
* The gateway has environment variables set for:
>* AF_IO_USER = "Adafruit.io user" - for AF.io access
>* AF_IO_KEY = "Adafruit.io API Key" - for AF.io access
>* SSK="Integer Key" this acts as a key to ensure that the data received by the gateway is data sent by a node on the LoRa network, and not some different LoRa transmission that happened to be on the same 915MHz band.
>* WEATHERBIT_API_KEY="API Key from Weatherbit.io"
* The Adafruit.io libraries were installed following the instructions [here](https://adafruit-io-python-client.readthedocs.io/en/latest/index.html).

### API Acess: 
#### Adafruit.io Cloud Storage and Dashboard Set-up
An API key from [Adafruit.io](https://io.adafruit.com/)(AF.io) is required. We use AF.io as a cloud data repository, and display the gathered data on [a dashboard](https://io.adafruit.com/IanJChadwick/dashboards/lora-wildfire-project).
* An AF.io feed was created for each data point (temperature, humidity, VPD, FWI, DMC and DC) for every node in order for the gateway to be able to transmit it to AF.io when it gets a packet from the node.
>* See the [AF.io documentation](https://io.adafruit.com/api/docs/#adafruit-io-http-api) or the [learning guide](https://learn.adafruit.com/series/adafruit-io-basics) to get instructions on how to use the AF.io platform and library.
* Additionally, a [dashboard](https://io.adafruit.com/IanJChadwick/dashboards/lora-wildfire-project) was created to provide a way to view the data. This dashboard was made public, so that anyone can view it, but options exist to make it private if desired.
#### [Weatherbit.io API](https://www.weatherbit.io/)
An API key is also required for weatherbit.io to gather the precipitation and wind data we needed to calculate the Fire Weather Index.

## Methodology
A high level overview of our methodology is described in the series of steps below:
1. Gather temperature and humidity data at 1 hour intervals
2. Package the data with SSK and NODE_ID into byte array for transmission over LoRa on the ISM 915MHz band
3. Gateway is continuously listening for LoRa packets on the 915MHz band but only moves to next steps if packet has matching SSK
4. Gateway receives data from nodes, unpacks it, calculates the VPD and uploads the data to appropriate Adafruit.io feeds based on NODE_ID
5. Once daily at noon the Fire Weather Index (FWI), and it's components, the Fine Fuel Moisture Code (FFMC), the Duff Moisture Code (DMC) and the Drought Code (DC) are calculated (as per the parameters specified for the [Fire Weather Index](https://cfs.nrcan.gc.ca/publications?id=19927)) and uploaded to AF.io
> * This calculation requires the previous 24-hour precipitation total and the wind speed which is gathered from the hourly weatherbit.io API
> * The calculation also requires the FFMC, DMC and DC from the previous day.
6. The data is then displayed on the AF.io Dashboard

### Wildfire Prediction Metrics and Calculations
* We determined that of the metrics that were described in the paper [(Impact of Anthropogenic Climate Change on Wildfire Across Western Forests)](https://www.pnas.org/content/113/42/11770), we would calculate the FWI (and the associated FFMC, DMC, and DC) in addition to the raw temperature and relative humidity readings from the sensor nodes.
* The other metrics, while useful in deterimining potential wildfire risk, were either too slow to take advantage of the hourly data being gathered, (i.e. on monthly timescales etc.) or did not utilize the temperature and humidity data that was being gathered in their calculations.

### Node Data Transmission
* Upon running the [node_data_tx.py](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/blob/main/PythonCode/node_data_tx.py) file, the nodes becomes a finite state machine with 3 states.
>1. The first state is the default "Ready" state and is indicated by "Ready" on the OLED display. This state is toggled by the left most button on the node.
>2. The second state is a single transmission state that sends the current sensor reading and returns to the Ready state. It is toggled by the middle button on the node.
>3. The third state is a continuous transmission state where the node will keep track of a monotonically increasing clock and transmit the current sensor reading every hour. It is toggled by the right most button on the node.
* The transmission is a bytearray with the NODE_ID and the SSK packaged with the temperature and relative humidity data from the AM2303 sensor.

### Data Receieved by Gateway
* Upon running the [hub_data_rx.py](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/blob/main/PythonCode/hub_data_rx.py) file, the gateway listens for a packet from a sensor node that has a matching SSK
* It decodes the packet and calculates the Vapor Pressure Deficit (VPD), and adds all three values to the correct feed associated with that node's ID.
* It then uploads the data to AF.io which displays the values from each of the nodes' feeds on the dashboard.
* Once daily, at noon the gateway retrieves the latest values from AF.io for Temperature, Humidity, the previous day's Fine Fuel Moisture Code (FFMC), Duff Moisture Code (DMC) and Drought Code (DC), as well as querries the weatherbit.io API for 24-hour precipitation total, and the average wind speed.
* It then utilizes the functions in [fire_weather_index.py](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/blob/main/PythonCode/fire_weather_index.py)in order to calculate the current day's FFMC, DMC and DC, and use these values along with the temperature, humidty, and month, to calculate the day's Fire Weather Index (FWI). (See the figure below for a graphical representation).
![Fire Weather Index Calculation Scheme](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/blob/main/Images/FWI%20Structure.JPG?raw=true "Structure of the CFWI System")
* It performs this caclulation for every node and associates the calculated values to the correct feed determined by the node ID.
* It then uploads all the newly calculated FWI data and associated components to AF.io where it is also displayed on the dashboard.


## [Wiki](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki) 
The wiki page has more detailed information about specfic pages for the:
* [Project Proposal](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Project-Proposal)
* [Hardware List](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Hardware)
* [Research and Resources](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Research-and-Resources)
* [APIs, Packages and Libraries](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/APIs,-Packages-and-Libraries)
