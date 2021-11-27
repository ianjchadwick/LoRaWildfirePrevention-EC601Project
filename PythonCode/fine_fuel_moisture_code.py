import xarray as xr
import numpy as np
"""
Modified code based on original code by: Josef Matondang:
 https://josefmtd.com/2021/07/06/computing-weather-data-with-python-netcdf4-and-xarray/
"""

class FineFuelMoistureCode:
    """
    Fine Fuel Moisture Code Calculation based on the
    Canadian Forest Fire Weather Index System using xarray
    """

    def __init__(self, temp, rhum, wind, rain, ffmc_prev):
        self.temp = temp
        self.rhum = rhum
        self.wind = wind
        self.rain = rain

        if type(ffmc_prev) == float or type(ffmc_prev) == int:
            self.ffmc_prev = rain.where(rain == ffmc_prev, other=ffmc_prev)
        else:
            self.ffmc_prev = ffmc_prev

    def compute(self):
        """
        Computes the FFMC through Raining Phase
        and Drying Phase

        Returns
        -------
        ffmc : xarray.DataArray
            today's FFMC
        """
        self.raining_phase()
        self.drying_phase()
        return self.ffmc

    def __moisture_content(self, ffmc):
        return 147.2 * (101.0 - ffmc) / (59.5 + ffmc)

    def __moisture_code(self, moisture):
        return 59.5 * (250.0 - moisture) / (147.2 + moisture)

    def __rain_normal(self, r_f, m_o):
        delta_m = (42.5 * np.exp(-100.0 / (251.0 - m_o)) * (1 - np.exp(-6.93 / r_f))) * r_f
        return m_o + delta_m

    def __rain_compensation(self, r_f, m_o):
        mr = self.__rain_normal(r_f, m_o)
        corrective = 0.0015 * (m_o - 150.0) ** 2 * r_f ** 0.5
        return mr + corrective

    def __no_rain(self, rain, m_o):
        return m_o + 0.0 * rain

    def raining_phase(self):
        """
        Moisture change due to rain from past 24 hours
        """
        # Moisture content before rain
        m_o = xr.apply_ufunc(self.__moisture_content, self.ffmc_prev)

        # Calculate effective rain due to canopy
        no_rain = self.rain.where(self.rain <= 0.5)
        effective_rain = xr.apply_ufunc(lambda x: x - 0.5, self.rain.where(self.rain > 0.5))

        # Use corrective equation for high moisture content
        compensation = m_o.where(m_o > 150.0)
        normal = m_o.where(m_o <= 150.0)

        mo_rc = xr.apply_ufunc(self.__rain_compensation, effective_rain, compensation)
        mo_r = xr.apply_ufunc(self.__rain_normal, effective_rain, normal)
        mo = xr.apply_ufunc(self.__no_rain, no_rain, m_o)

        self.mr = mo_r.fillna(0) + mo_rc.fillna(0) + mo.fillna(0)
        self.mr.rename('moisture_after_rain')

    def __drying(self, mr, E_d, k_d):
        return E_d + (mr - E_d) / 10 ** k_d

    def __wetting(self, mr, E_w, k_w):
        return E_w - (E_w - mr) / 10 ** k_w

    def drying_phase(self):
        """
        Moisture change due to drying phase from noon to afternoon
        """
        # Equilibrium moisture content for drying and wetting phase
        E_d = 0.942 * self.rhum ** 0.679 + \
              11.0 * np.exp((self.rhum - 100.0) / 10) + \
              0.18 * (21.1 - self.temp) * (1 - np.exp(-0.115 * self.rhum))
        E_w = 0.618 * self.rhum ** 0.753 + \
              10.0 * np.exp((self.rhum - 100.0) / 10) + \
              0.18 * (21.1 - self.temp) * (1 - np.exp(-0.115 * self.rhum))

        # Calculate the log drying/wetting rate
        k_1 = 0.424 * (1 - ((100.0 - self.rhum) / 100.0) ** 1.7) + \
              0.0694 * self.wind ** 0.5 * \
              (1 - ((100.0 - self.rhum) / 100.0) ** 8)
        k_0 = 0.424 * (1 - ((100.0 - self.rhum) / 100.0) ** 1.7) + \
              0.0694 * self.wind ** 0.5 * \
              (1 - (self.rhum / 100) ** 8)
        k_d = k_0 * 0.581 * np.exp(0.0365 * self.temp)
        k_w = k_1 * 0.581 * np.exp(0.0365 * self.temp)

        # Wetting and drying conditions
        drying = self.mr.where(self.mr > E_d)
        wetting = self.mr.where(self.mr < E_w)
        no_change = self.mr.where((self.mr >= E_w) & (self.mr <= E_d))

        # Moisture content after drying
        m_d = xr.apply_ufunc(self.__drying, drying, E_d, k_d)
        m_w = xr.apply_ufunc(self.__wetting, wetting, E_w, k_w)
        m = m_d.fillna(0) + m_w.fillna(0) + no_change.fillna(0)

        # Calculate Fine Fuel Moisture Code
        self.ffmc = xr.apply_ufunc(self.__moisture_code, m)
        self.ffmc = self.ffmc.rename('fine_fuel_moisture_code')

if __name__ == '__main__':
    ffmc_prev = 85.0
    temp = 24
    rhum = 65
    wind = 1.34
    rain = 0
    ffmc_calc = FineFuelMoistureCode(temp, rhum, wind, rain, ffmc_prev)
    ffmc = ffmc_calc.compute()