# EC601Project1 - WAN
Exploration of low-cost LoRaWAN based wide-area distributed sensor networks for prediction and prevention of wildfires.

## Problem Statement

Wildfire occurances have been increasing in frequency and severity over the last several decades. The areas prone to forest fires has doubled from 1984 to 2015, indicating a trend of increasing risk of catastrophic wildfire events.[(1)](https://www.pnas.org/content/113/42/11770) The economic impact has been especially exemplified in California, where the fires in 2018 alone have led to an estimated loss of approximately $150 billion, when far reaching factors such as health impacts of wildfire smoke and supply chain interruptions are considered. [(2)](https://doi.org/10.1038/s41893-020-00646-7) This is an estimated 1.5% loss of the total GDP of California, and 0.5% loss of the total GDP of the United States.

Some of the long reaching effects of these losses are the "hardening" of the reinsurance market[(3)](https://www.actuaries.digital/2021/04/29/a-hardening-reinsurance-market-how-to-mitigate-the-adverse-impact/), which will cause securing adequate insurance coverage to become more costly and difficult, and the increasing cost of building materials[(4)](https://www.businessobserverfl.com/article/from-home-improvement-to-home-building-shortages-causing-major-delays-and-cancellations-for-builders-and-contractors), which will have the a similar effect on increasing the cost of post-disaster reconstruction effors. There are many other deterimental impacts, such as the increased input of atmospheric carbon on climate change and the psychosocial impact of wildfires that are more difficult to quantify and will likely be explored as these events continue to become more common.

Approximately 84% of wildfires in the United States are caused by human activity[(5)](https://www.pnas.org/content/114/11/2946), from a variety of disparate causes ranging from negligence, to faulty and malfunctioning equipment.[(6)](https://www.fs.usda.gov/rds/archive/Catalog/RDS-2013-0009.5) This indicates that pivoting from a reactionary rebuilding stance, to a proactive early prediction, detection and prevention stance could have a profound impact on the mitigation of extremely costly wildfire events.

## Proposed Solution

Predictive models based on forest soil moisture, temperature and previously burned areas provide 83.4% accuracy based on satellite data provides an excellent basis for the creation of a wide area sensor network to gather the data needed for an even more accurate prediction.[(7)](https://ieeexplore.ieee.org/document/7503172) My proposal is to use a similar predictive model with a Long-Range Wide Area Networks (LoRaWAN) based system of low-cost and low-power moisture and temperature sensors distributed across high risk areas. I postulate that this would provide very precise and accurate data that can be leveraged to predict the regions that are most likely to have a wildfire incident. This information can be used by local government and fire authorities to base policy and resource allocation decisions to mitigate the overall damage of wildfires. In addition, the data gathered can alert the proper authorities of a wildfire occurance while it is still relatively small, increasing the chances of an early containment.

### Specifications/Requirements and LoRaWAN

For this proposal, I will be using Califonia as the primary basis for exploratory analysis and cost estimates, primarily because of the avialbility of data, studies and that many of the severe wildfires that have occured within the past decade in the Western United States have occured within the state.

In order for this porposal to be feasible, there are several requirements that would need to be met. The system and associated devices need:
1. Low-Cost
2. Low-Power
3. Cover a wide area
4. Provide accurate data 
5. Provide data at a relatively frequent rate
6. Secure

In terms of the available IoT technolgy used to implement the system, LoRaWAN has many properties that make it an ideal candidate based on the requirements of the system when compared to other IoT connectivity standards.[(8)](https://www.iot-now.com/2020/12/23/106701-lorawan-will-temporarily-replace-5g-networks-for-iot/) LoRa sensors

### References
1. [Abatzoglou, J. T. & Williams, A. P. Impact of anthropogenic climate change on wildfire across western US forests. Proc. Natl Acad. Sci. USA 113, 11770–11775 (2016).](https://www.pnas.org/content/113/42/11770)
2. [Wang, D., Guan, D., Zhu, S. et al. Economic footprint of California wildfires in 2018. Nat Sustain 4, 252–260 (2021).](https://doi.org/10.1038/s41893-020-00646-7)
3. [S. Jinadasa and T. Y. Siang. "A “Hardening” Reinsurance Market – How to Mitigate the Adverse Impact" https://www.actuaries.digital, Apr. 29, 2021. (Online). Available: https://www.actuaries.digital/2021/04/29/a-hardening-reinsurance-market-how-to-mitigate-the-adverse-impact/ (Accessed Sept. 18, 2021).](https://www.actuaries.digital/2021/04/29/a-hardening-reinsurance-market-how-to-mitigate-the-adverse-impact/)
4. [L. Lovio, "From home improvement to home building, shortages causing major delays — and cancellations — for builders and contractors" https://www.businessobserverfl.com/, Jun. 3, 2021. (Online). Available: https://www.businessobserverfl.com/article/from-home-improvement-to-home-building-shortages-causing-major-delays-and-cancellations-for-builders-and-contractors (Accessed Sept 18, 2021)](https://www.businessobserverfl.com/article/from-home-improvement-to-home-building-shortages-causing-major-delays-and-cancellations-for-builders-and-contractors)
5. [Balch, J. K., Bradley B. A., Abatzoglou, J. T., Nagy, R. C., Fusco, E. J., Mahood, A. L.,  Human-started wildfires expand the fire niche across the United States. Proc. Natl. Acad. Sci. USA 114 (11) 2946-2951 (2017)](https://www.pnas.org/content/114/11/2946)
6. [Short, Karen C. 2021. Spatial wildfire occurrence data for the United States, 1992-2018 [FPA_FOD_20210617]. 5th Edition. Fort Collins, CO: Forest Service Research Data Archive. https://doi.org/10.2737/RDS-2013-0009.5](https://www.fs.usda.gov/rds/archive/Catalog/RDS-2013-0009.5)
7. [D. Chaparro, M. Vall-llossera, M. Piles, A. Camps, C. Rüdiger and R. Riera-Tatché, "Predicting the Extent of Wildfires Using Remotely Sensed Soil Moisture and Temperature Trends," in IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, vol. 9, no. 6, pp. 2818-2829, June 2016, doi: 10.1109/JSTARS.2016.2571838.](https://ieeexplore.ieee.org/document/7503172)
8. [Seletsky S.,"LoRaWAN will temporarily replace 5G networks for IoT" https://www.iot-now.com/, Dec. 23, 2020. (Online). Available: https://www.iot-now.com/2020/12/23/106701-lorawan-will-temporarily-replace-5g-networks-for-iot/ (Accessed: September 18, 2021)](https://www.iot-now.com/2020/12/23/106701-lorawan-will-temporarily-replace-5g-networks-for-iot/)
