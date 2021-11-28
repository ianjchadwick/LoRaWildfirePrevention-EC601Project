import xarray as xr
import numpy as np
import math
"""
Modified code based on R code from: Grant Williamson:
 http://www.atriplex.info/index.php/Fire_Danger_Index_Functions_in_R#Canadian_Fire_Weather_Index
"""

"""
Function to calculate the Fine Fuel Moisture Code (FFMC)
inputs: temperature (C), relative humidity (%), average wind speed (m/s), previous day's FFMC (default 85), previous 
24-hour precipitation total (mm)

Output: Today's FFMC
"""
def fine_fuel_moisture_code(temp, rel_hum, avg_wind, precip, F_prev = 85):

    # Get previous day's FFMC and default to 85 if not entered
    Fo = F_prev

    # Previous day's moisture content
    mo = 147.2*(101-Fo)/(59.5+Fo)

    # Adjust mo for rain
    if (precip > 0.5):
        rf = precip - 0.5
        if mo <= 150:
            mr = mo + 42.5 * rf * math.exp((-100/(251-mo))) * (1 - math.exp(-6.93/rf))
        else:
            mr = mo + 42.5 * rf * math.exp((-100/(251-mo))) * (1 - math.exp(-6.93/rf)) + \
                 0.0015*(math.pow((mo-150), 2))*math.pow(rf, 0.5)
        if mr > 250:
            mr = 250
        mo = mr

    ko = 0.424*(1 - math.pow((100-rel_hum)/100, 1.7)) + (0.0694* avg_wind^0.5)*(1 - math.pow((100-rel_hum)/100, 8))

    k = ko * 0.581*math.exp(0.0365*temp)

    Ed = 0.942*math.pow(rel_hum, 0.679) + 11*math.exp((rel_hum - 100)/10) + \
         0.18*(21.1-temp)*(1-math.exp(-0.115*rel_hum))

    Ew = 0.618*math.pow(rel_hum, 0.753) + 10*math.exp((rel_hum-100)/10) + 0.18*(21.1-temp)(1-math.exp(-0.115*rel_hum))

    # If moisture is greater than Ed, than drying regime calculation takes place
    if Ed < mo:
        m = Ed + (mo - Ed)*math.pow(10, (-1*k))

    # If moisture is less than Ew, than wetting regime calculation takes place
    elif mo < Ew & mo < Ed:
        m = Ew - (Ew - mo)*math.pow(10, (-1*k))

    # Else if the moisture content is between the two values, previous moisture content is today's content
    elif Ed >= mo & Ew <= mo:
        m = mo

    FFMC = 59.5* (250-m)/(147.2 + m)

    return FFMC

"""
Function to calculate the Duff Moisture Code (DMC)
Inputs: relative humidity (%), temperature (C), 24-hour precipitation total (mm), current month (int format), previous
day's DMC (default=6).

Output: Today's DMC
"""
def duff_moisture_code(rel_hum, temp, precip, month, DMC_prev=6.0):
    Po = DMC_prev
    DayLengthList = [6.5, 7.5, 9.0, 12.8, 13.9, 13.9, 12.4, 10.9, 9.4, 8.0, 7.0, 6.0]
    effDayLength = DayLengthList[month-1]

    # If rainfall greater than 1.5mm adjust previous day's moisture content
    if precip > 1.5:
        # Calculate effective precipitation
        effPrecip = 0.92*precip -1.27

        # Previous day's duff moisture content
        Mo = 20 + math.exp(5.6348 - (Po/43.43))

        # Calculate the slope variable 'b'
        if Po <= 33:
            b = 100/(0.5 + 0.3*Po)
        elif Po > 33 & Po <= 65:
            b = 14 - 1.3*math.log(Po)
        else:
            b = 6.2*math.log(Po) - 17.2

        # Calculate moisture content after rain
        Mr = Mo + (1000*effPrecip)/(48.77+b*effPrecip)

        # Calculate the moisture content after rain 'Pr'
        Pr = 244.72 - 43.43 * math.log(Mr-20)
        if Pr < 0:
            Pr = 0

        Po = Pr

    # Log drying rate for DMC
    if temp < -1.1:
       temp = -1.1
    K = 1.894*(temp+1.1)*(100-rel_hum)*effDayLength*math.pow(10, -6)

    DMC = Po + 100*K

    return DMC


"""
Function to cacluclate the Drought Code (DC)
Inputs: previous day's DC (default=15),  24-hour precipitation total (mm), temperature (C), month (as integer)
Output: Today's DC
"""
def drought_code(temp, precip, month, DC_prev=15):
    DayLengthList = [-1.6, -1.6, -1.6, 0.9, 3.8, 5.8, 6.4, 5.0, 2.4, 0.4, -1.6, -1.6]
    dayLengthFactor = DayLengthList[month-1]
    Do = DC_prev

    # Adjust Do for rain > 2.8mm

    if precip > 2.8:
        # Effective rainfall
        Pd = 0.93*precip - 1.27

        # Moisture equivalent of Do
        Qo = 800*math.exp((-1*Do/400))

        # Moisture after rain
        Qr = Qo +3.937*Pd

        # DC after rain
        Dr = 400*math.log(800/Qr)
        if Dr < 0:
            Dr = 0
        Do = Dr

    # Potential Evapotranspiration
    if temp < -2.8:
        temp = -2.8
    V = 0.36*(temp+2.8)+dayLengthFactor
    if V < 0:
        V = 0

    DC = Do + 0.5*V
    return DC


