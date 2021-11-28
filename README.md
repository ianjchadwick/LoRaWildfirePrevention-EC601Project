# LoRa Wildfire Prevention Project - EC601

## Goal
Our objective is to build a proof-of-concept IoT system of low-power, low-cost sensor nodes which measure temperature and relative humidity data, and use this data to refine remote sensing data in order to improve the accuracy of existing wildfire prediction models. See the [original proposal in the wiki](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Project-Proposal) for more details.

## Methodology
* The project was implemented using the AGILE framework (see the [project page](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/projects/1) for kanban board) over the course of five two-week sprints.
* We utilized RaspberryPi Zero based sensor nodes with a LoRa radio transciever hat and an AM2302 sensor to record temperature and relative humidity data, and transmit it via LoRa to a central gateway every 30 minutes. 
* The gateway is a RaspberryPi 3 with the same LoRa transceiver radio module which receives the data from the nodes and uploads it to Adafruit.io. 
* We use Adafruit.io as a cloud data repository, and display the gathered data on [a dashboard](https://io.adafruit.com/IanJChadwick/dashboards/lora-wildfire-project).
* We then gathered weather station data from the [Weatherbit.io Current Weather API](https://www.weatherbit.io/api/weather-current) to supplement the in-situ temperature and relative humidity data.

## [Wiki](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki) 
The wiki page has more detailed information about specfic pages for the:
* [Project Proposal](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Project-Proposal)
* [Hardware List](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Hardware)
* [Research and Guides](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/Research-and-Guides)
* [APIs, Packages and Libraries](https://github.com/ianjchadwick/LoRaWildfirePrevention-EC601Project/wiki/APIs,-Packages-and-Libraries)
