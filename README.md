# EC601Project1 - LoRaWAN for Wildfire Prediction and Prevention
Exploration of Low-Power Wide-Area(LPWA) IoT connection standards (Long Range WAN (LoRaWAN specifically) for a wide-area distributed sensor network to predict and prevent wildfires.

## Problem Statement

Wildfire occurances have been increasing in frequency and severity over the last several decades. The areas prone to forest fires has doubled from 1984 to 2015, indicating a trend of increasing risk of catastrophic wildfire events.[(1)](https://www.pnas.org/content/113/42/11770) The economic impact has been especially exemplified in California, where the fires in 2018 alone have led to an estimated loss of approximately $150 billion, when far reaching factors such as health impacts of wildfire smoke and supply chain interruptions are considered. [(2)](https://doi.org/10.1038/s41893-020-00646-7) This is an estimated 1.5% loss of the total GDP of California, and 0.5% loss of the total GDP of the United States.

Some of the long reaching effects of these losses are the "hardening" of the reinsurance market[(3)](https://www.actuaries.digital/2021/04/29/a-hardening-reinsurance-market-how-to-mitigate-the-adverse-impact/), which will cause securing adequate insurance coverage to become more costly and difficult, and the increasing cost of building materials[(4)](https://www.businessobserverfl.com/article/from-home-improvement-to-home-building-shortages-causing-major-delays-and-cancellations-for-builders-and-contractors), which will have the a similar effect on increasing the cost of post-disaster reconstruction effors. There are many other deterimental impacts, such as the increased input of atmospheric carbon on climate change and the psychosocial impact of wildfires that are more difficult to quantify and will likely be explored as these events continue to become more common.

Approximately 84% of wildfires in the United States are caused by human activity[(5)](https://www.pnas.org/content/114/11/2946), from a variety of disparate causes ranging from negligence, to faulty and malfunctioning equipment.[(6)](https://www.fs.usda.gov/rds/archive/Catalog/RDS-2013-0009.5) This indicates that pivoting from a reactionary rebuilding stance, to a proactive early prediction, detection and prevention stance could have a profound impact on the mitigation of extremely costly wildfire events.

## Proposed Solution

Predictive models based on forest soil moisture, temperature and previously burned areas provide 83.4% accuracy based on satellite data provides an excellent basis for the creation of a wide area sensor network to gather the data needed for an even more accurate prediction.[(7)](https://ieeexplore.ieee.org/document/7503172) My proposal is to use a similar predictive model with a Long-Range Wide Area Networks (LoRaWAN) based system of low-cost and low-power moisture and temperature sensors distributed across high risk areas. I postulate that this would provide very precise and accurate data that can be leveraged to predict the regions that are most likely to have a wildfire incident. This information can be used by local government and fire authorities to base policy and resource allocation decisions to mitigate the overall damage of wildfires. In addition, the data gathered can alert the proper authorities of a wildfire occurance while it is still relatively small, increasing the chances of an early containment.

### Specifications/Requirements and LoRaWAN

For this proposal, I will be using Califonia and USD as the primary basis for exploratory analysis and cost estimates, primarily because of the avialbility of data, studies and that many of the severe wildfires that have occured within the past decade in the Western United States have occured within the state.

In order for this porposal to be feasible, there are several requirements that would need to be met. The system and associated devices need:
1. Low-Cost
2. Low-Power
3. Cover a wide area
4. Provide accurate data at a relatively frequent rate
5. Secure
6. Wide support

In terms of the available IoT technolgy used to implement the system, LoRaWAN has many properties that make it an ideal candidate based on the requirements of the system when compared to other IoT connectivity standards.[(8)](https://www.iot-now.com/2020/12/23/106701-lorawan-will-temporarily-replace-5g-networks-for-iot/) 

**Low-Cost and Wide Area:** Cost is will be the primary challenge to overcome for widespread adoption of the system and the cost will increase proportionally with the area covered. Fortunately, LoRa sensors and base stations are inexpensive, with an estimated cost ranging from $0.20-$0.50/sensor and around $40.00/base station. Base stations can handle thousands of connections within a 15km range. Considering California is approximately 263,500 square kilometers, 17,563 base stations would cost $702,520 and if every square kilometer had two sensors, would require 527,000 sensors ranging from $105,400-$263,500. The total cost of hardware would be roughly $808k-966k but would cover ever square kilometer of the state. This "back of napkin calculation" is a gross oversimplification considering a large portion of the state would not require sensors because they are not at risk of wildfire (i..e deserts, lakes, areas within established cities and towns), but it provides a good conceptual framework to compare the costs of catastrophic wildfires (in the order of tens to hundreds of billions of dollars) to prevention (in the order of millions to tens of millions of dollars).

**Low-Power:** LoRaWAN devices have another advantage over some of the other connectivity standards in that they can run for up to 10 years on a single battery, increasing the logevity of the sensors.

**Accurate and Frequent Data:** One of the preceived drawbacks of LoRa is that it has liomited bandwith and can only transmit short packages of data (about 240 bytes), but for this use case, that isn't as much of a limiting factor as it is for other use cases since the devices would only need to transmit temperature and humidity data. Additionally, while LoRa is not effective for continuous real-time monitoring it is very effective for gathering and transmitting relatively frequent data at specified times. The amount of times each sensor transmits can be determined based on an analysis based on desired data accuracy weighed against power consumption.

**Secure:** Security is an important consideration for any IoT device, especially one with serious health and safety considerations. Fortunately, the security of LoRaWAN is very robust and utilizes full end-to-end encryption, ensuring that malicious actors cannot interfere with the network.

**Wide Support:** The [LoRa Alliance](https://lora-alliance.org/) is a non-profit organization dedicated to increasing the use of LoRa for IoT applications and has members including IBM, Cisco and has been deployed in over 100 countries worldwide. Additionally, the LoRa Alliance provides standards and documentation for the LoRa protocol making it possible for developers to create new applications of the technology.

## Conclusion

Wildfires have had severe economic reprecussions and have been increasing in frequency and severatiy over the past several decades. A solution to the problem is to use a distributed sensor network to gather data and predict the likelihood of wildfires and potentially stop them from causing catastrophic damage. LoRaWAN based devices offer a cheap and effective way to provide environmental temperature and humidity data at a much more granular level than satellite data. These data can  be used with predictive models to determine where wildfire occurances are more likely, which can help local authorities and governments determine the best way to allocate the already strained wildfire fighting resources and reduce the overall costs of wildfires.


### References
1. [Abatzoglou, J. T. & Williams, A. P. Impact of anthropogenic climate change on wildfire across western US forests. Proc. Natl Acad. Sci. USA 113, 11770–11775 (2016).](https://www.pnas.org/content/113/42/11770)
2. [Wang, D., Guan, D., Zhu, S. et al. Economic footprint of California wildfires in 2018. Nat Sustain 4, 252–260 (2021).](https://doi.org/10.1038/s41893-020-00646-7)
3. [S. Jinadasa and T. Y. Siang. "A “Hardening” Reinsurance Market – How to Mitigate the Adverse Impact" https://www.actuaries.digital, Apr. 29, 2021. (Online). Available: https://www.actuaries.digital/2021/04/29/a-hardening-reinsurance-market-how-to-mitigate-the-adverse-impact/ (Accessed Sept. 18, 2021).](https://www.actuaries.digital/2021/04/29/a-hardening-reinsurance-market-how-to-mitigate-the-adverse-impact/)
4. [L. Lovio, "From home improvement to home building, shortages causing major delays — and cancellations — for builders and contractors" https://www.businessobserverfl.com/, Jun. 3, 2021. (Online). Available: https://www.businessobserverfl.com/article/from-home-improvement-to-home-building-shortages-causing-major-delays-and-cancellations-for-builders-and-contractors (Accessed Sept 18, 2021)](https://www.businessobserverfl.com/article/from-home-improvement-to-home-building-shortages-causing-major-delays-and-cancellations-for-builders-and-contractors)
5. [Balch, J. K., Bradley B. A., Abatzoglou, J. T., Nagy, R. C., Fusco, E. J., Mahood, A. L.,  Human-started wildfires expand the fire niche across the United States. Proc. Natl. Acad. Sci. USA 114 (11) 2946-2951 (2017)](https://www.pnas.org/content/114/11/2946)
6. [Short, Karen C. 2021. Spatial wildfire occurrence data for the United States, 1992-2018 [FPA_FOD_20210617]. 5th Edition. Fort Collins, CO: Forest Service Research Data Archive. https://doi.org/10.2737/RDS-2013-0009.5](https://www.fs.usda.gov/rds/archive/Catalog/RDS-2013-0009.5)
7. [D. Chaparro, M. Vall-llossera, M. Piles, A. Camps, C. Rüdiger and R. Riera-Tatché, "Predicting the Extent of Wildfires Using Remotely Sensed Soil Moisture and Temperature Trends," in IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, vol. 9, no. 6, pp. 2818-2829, June 2016, doi: 10.1109/JSTARS.2016.2571838.](https://ieeexplore.ieee.org/document/7503172)
8. [Seletsky S.,"LoRaWAN will temporarily replace 5G networks for IoT" https://www.iot-now.com/, Dec. 23, 2020. (Online). Available: https://www.iot-now.com/2020/12/23/106701-lorawan-will-temporarily-replace-5g-networks-for-iot/ (Accessed: September 18, 2021)](https://www.iot-now.com/2020/12/23/106701-lorawan-will-temporarily-replace-5g-networks-for-iot/)
