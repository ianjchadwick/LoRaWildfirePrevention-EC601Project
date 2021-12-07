import math
"""
Modified code based on R code from: Grant Williamson:
 http://www.atriplex.info/index.php/Fire_Danger_Index_Functions_in_R#Canadian_Fire_Weather_Index
"""

"""
Function to calculate the Fine Fuel Moisture Code (FFMC)

Inputs: temperature (C), 
        relative realtime humidity (%), 
        average wind speed (m/s), 
        previous day's FFMC (default 85), previous 
        24-hour precipitation total (mm)
        
Output: Today's FFMC
"""
class Fire_Weather_Index:

    def __init__(self):
        print("Access Fire Weather Index Calculation: ")

    def fine_fuel_moisture_code(self, temp, rel_hum, avg_wind, precip, F_prev = 85.0):

        # Get previous day's FFMC and default to 85 if not entered
        Fo = F_prev

        # Previous day's moisture content
        moisture = 147.2*(101-Fo)/(59.5+Fo)

        # Adjust moisture for rain, if rainfall greater than 0.5mm
        if (precip > 0.5):
            rf = precip - 0.5

            mr = moisture + 42.5 * rf * math.exp((-100/(251-moisture))) * (1 - math.exp(-6.93/rf))

            if moisture > 150:
                mr = mr + 0.0015*(math.pow((moisture-150), 2))*math.pow(rf, 0.5)

            if mr > 250:
                mr = 250
            moisture = mr

        ko = 0.424*(1 - math.pow((100-rel_hum)/100, 1.7)) + \
            (0.0694* math.pow(avg_wind, 0.5)) * (1 - math.pow((100-rel_hum)/100, 8))

        k = ko * 0.581*math.exp(0.0365*temp)

        Ed = 0.942 * math.pow(rel_hum, 0.679) + 11 * math.exp((rel_hum - 100)/10) + \
             0.18 * (21.1-temp) * (1-math.exp(-0.115*rel_hum))

        Ew = 0.618 * math.pow(rel_hum, 0.753) + 10 * math.exp((rel_hum-100)/10) + \
             0.18 * (21.1-temp) * (1-math.exp(-0.115*rel_hum))

        m_current = float

        # Equilibrium Mosture Content: log( Realistic Moisture - Tree Moisture Content)
        #
        # If yesterday‘s moisture is greater than Ed: (Equilibrium Moisture Content obtained by drying)
        # than drying regime calculation takes place

        if moisture > Ed:
            m_current = Ed + (moisture - Ed) * math.pow(10, (-1*k))

        # If yesterday's moisture is lesser than Ew: (Equilibrium Moisture Content obtained by wetting),
        # then wetting regime calculation takes place

        elif (moisture < Ew) and (moisture < Ed):
            m_current = Ew - (Ew - moisture) * math.pow(10, (-1*k))

        # Else if the moisture content is between the two values, previous moisture content is today's content
        elif (Ed >= moisture) and (Ew <= moisture):
            m_current = moisture

        FFMC = 59.5 * (250 - m_current) / (147.2 + m_current)

        return FFMC


    """
    Function to calculate the Duff Moisture Code (DMC)
    Inputs: relative humidity (%), 
            temperature (C), 
            24-hour precipitation total (mm), 
            current month (int format), 
            previous day's DMC (default=6).
    
    Output: Today's DMC
    """
    def duff_moisture_code(self, rel_hum, temp, precip, month, DMC_prev=6.0):
        Po = DMC_prev
        month = int(month)
        DayLengthList = [6.5, 7.5, 9.0, 12.8, 13.9, 13.9, 12.4, 10.9, 9.4, 8.0, 7.0, 6.0]

        effDayLength = DayLengthList[month-1]

        # If rainfall greater than 1.5mm adjust previous day's moisture content
        if precip > 1.5:
            # Calculate effective precipitation
            effPrecip = 0.92*precip -1.27

            # Previous day's duff moisture content
            Mo = 20 + math.exp(5.6348 - (Po / 43.43))

            # Calculate the slope variable 'b'
            if Po <= 33:
                b = 100/(0.5 + 0.3*Po)
            elif Po > 33 and Po <= 65:
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

        DMC = Po + 100 * K

        return DMC


    """
    Function to cacluclate the Drought Code (DC)
    Inputs: previous day's DC (default=15),  
            24-hour precipitation total (mm), 
            temperature (C), 
            month (as integer)
            
    Output: Today's DC
    """
    def drought_code(self, temp, precip, month, DC_prev=15):
        DayLengthList = [-1.6, -1.6, -1.6, 0.9, 3.8, 5.8, 6.4, 5.0, 2.4, 0.4, -1.6, -1.6]
        month = int(month)
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

    """
    Function to calculate the Initial Spread Index (ISI)
    Inputs: FFMC and Wind speed
    
    Outputs: ISI
    """
    def initial_spread_index(self, FFMC, wind):
        # Wind function
        fW  = math.exp(0.05039*wind)

        # Get moisture from FFMC
        m = 147.2*(101-FFMC)/(59.5 + FFMC)

        # FFMC function

        fF = (91.9*math.exp(-0.1386*m))*(1 + math.pow(m, 5.31)/(4.93*math.pow(10, 7)))

        ISI = 0.208*fW*fF

        return ISI


    """
    Function to calculate the Buildup Index (BUI)
    Inputs: DMC and DC
    
    Outputs: BUI
    """
    def buildup_index(self, DMC, DC):
        # If the DMC is 0 BUI is always 0
        if DMC == 0:
            BUI = 0
            return BUI
        if DMC <= 0.4*DC:
            BUI = 0.8 * DMC * DC / (DMC + 0.4 * DC)
        else:
            BUI = DMC - (1 - 0.8*DMC/ (DMC + 0.4*DC)) * (0.92 + math.pow((0.0114*DMC), 1.7))

        return BUI

    """
    
    Final function to calculate the fire weather index FWI:
    Inputs: temp: temperature (C), 
            rel_hum: relative humidity (%),
            wind: average wind speed (m/s), 
            precip: previous 24-hour precipitation total (mm),  
            month: month (as integer), 
            DMC: previous day's DMC (default=6),
            FFMC: previous day's FFMC (default 85), 
            DC: previous day's DC (default=15)
            
    Output: A scale value under a certain level between 1 - 10 of Fire Weather Index
    
    """
    def fire_weather_index(self, temp, rel_hum, wind, precip , month, DMC=6.0, FFMC=85.0, DC=15.0):

        finefuelMC = self.fine_fuel_moisture_code(temp, rel_hum,wind, precip, FFMC)
        duffMC = self.duff_moisture_code(rel_hum, temp, precip, month, DMC)
        droughtC = self.drought_code(temp, precip, month, DC)
        ISI = self.initial_spread_index(finefuelMC, wind)
        BUI = self.buildup_index(duffMC, droughtC)

        if BUI <= 80:
            fD = 0.626 * math.pow(BUI,0.809) + 2
        if BUI > 80:
            fD = 1000/(25 + 108.64*math.exp(-0.023*BUI))

        Bscale = 0.1 * ISI * fD

        if Bscale <= 1:
            Sscale = Bscale
        else:
            Sscale = math.exp(2.72 * math.pow((0.434*math.log(Bscale)), 0.647))

        return Sscale
