# LoRa Wildfire Prevention Project - EC601

## Goal
Our objective is to build a proof-of-concept IoT system of low-power, low-cost sensor nodes which measure temperature and relative humidity data, and use this data to refine remote sensing data in order to improve the accuracy of existing wildfire prediction models. Our hope is that more data will allow decision makers and stakeholders, such as firefighting organizations and local government officials to allocate resources more efficiently, in hopes of preventing catastrophic wildfire losses. See the [original proposal in the wiki](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Project-Proposal) for more details.

## Methodology
### Project Management
* The project was implemented using the AGILE framework (see the [project page](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/projects/1) for kanban board) over the course of five two-week sprints.

### Hardware Set-Up
#### Sensor Nodes
We utilized RaspberryPi Zero based sensor nodes with a LoRa radio transciever hat and an AM2302 sensor to record temperature and relative humidity data, and transmit it via LoRa on the ISM 915MHz band to a central gateway every 60 minutes.
* We used a [RaspberryPI Zero](https://www.adafruit.com/product/3708) with headers installed as the base for the other breakouts.
* A [LoRa radio transceiver module](https://www.adafruit.com/product/4074) was added to the Pi via the headers.
* An [AM2302 temperature and humidity sensor](https://www.adafruit.com/product/393) was soldered to GPIO pin 4, the 5V, and GND on the LoRa tansceiver module.
* An on/off switch, and the USB-A jack was was soldered to the [PowerBoost chip](https://www.adafruit.com/product/1903) (see [this link](https://learn.adafruit.com/adafruit-powerboost-500-plus-charger/on-slash-off-switch) for specifics)]
* The [900MHz antenna](https://www.adafruit.com/product/3340) was attached to the uFL port on the LoRa module
* A 2000mAh 3.7V LiPo battery was connected to the PowerBoost chip via the JST connector and the USB-A jack was connected to the Pi Zero's power-in USB-B port.
#### Gateway
The gateway receives and decodes the data from the nodes, performs the calculations to determine the meterics for Fire Weather Index (and the components FFMC, DMC and DC), Vapor Pressure Deficit (VPD), and uploads the data to Adafruit.io.
* We used a [Rasberry Pi 3 B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/) as the base for the breakouts to build the gateway.
* Similarly to the nodes, a [LoRa radio transceiver module](https://www.adafruit.com/product/4074) was added to the Pi 3 via the headers.
* Again, the [900MHz antenna](https://www.adafruit.com/product/3340) was attached to the uFL port on the LoRa module.
* The Pi was connected to power via a USB-B 5V wall outlet.

### Software Set-Up
The nodes and gateways are running the Raspbian operating system with the CircuitPython libraries for the firmware for the LoRa radio module and AM2302 sensors.
* [RasbianOS](https://www.raspberrypi.com/software/) was installed on an 8GB SD card for the nodes and a 32GB SD card for the gateway.
* CircuitPython was installed on the gateway and each of the nodes following the [outline provided here](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi).
* Then the radio modules were set-up by installing the necessary modules [discussed here](https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi/rfm9x-raspberry-pi-setup).
* The DHT22 sensor module was insalled utilizing [the adafruit circuit python libraries](https://learn.adafruit.com/dht/dht-circuitpython-code)
#### Node -specific Software Set-up
* The nodes each have environments variable set for: 
>* NODE_ID="unique integer" this ID identifies the node so that its location and data values can be determined by the gateway
>* SSK="Integer Key" this acts as a key to ensure that the data received by the gateway is data sent by a node on the LoRa network, and not some different LoRa transmission that happened to be on the same 915MHz band.
* The nodes then have [node_data_tx.py from PythonCode](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/blob/main/PythonCode/node_data_tx.py) in the same directory as the set-up files for CircuitPython (and font5x8.bin file required for the OLED).
#### Gateway-specific Software Set-up
* The gateway has environment variables set for:
>* AF_IO_USER = "Adafruit.io user" - for AF.io access
>* AF_IO_KEY = "Adafruit.io API Key" - for AF.io access
>* SSK="Integer Key" this acts as a key to ensure that the data received by the gateway is data sent by a node on the LoRa network, and not some different LoRa transmission that happened to be on the same 915MHz band.
>* WEATHERBIT_API_KEY="API Key from Weatherbit.io"
* The Adafruit.io libraries were installed following the instructions [here](https://adafruit-io-python-client.readthedocs.io/en/latest/index.html).

### Adafruit.io Cloud Storage and Dashboard
We use Adafruit.io (AF.io) as a cloud data repository, and display the gathered data on [a dashboard](https://io.adafruit.com/IanJChadwick/dashboards/lora-wildfire-project).
* An AF.io feed was created for each data point (temperature, humidity, VPD, FWI, DMC and DC) of every node 
* We then gathered weather station data from the [Weatherbit.io Current Weather API](https://www.weatherbit.io/api/weather-current) to supplement the in-situ temperature and relative humidity data.

## [Wiki](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki) 
The wiki page has more detailed information about specfic pages for the:
* [Project Proposal](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Project-Proposal)
* [Hardware List](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Hardware)
* [Research and Resources](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Research-and-Resources)
* [APIs, Packages and Libraries](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/APIs,-Packages-and-Libraries)
