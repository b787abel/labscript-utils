from .UnitConversionBase import *
from scipy.interpolate import interp1d
import numpy as np 

class R780AOMFreqConv(UnitConversion):
    base_unit = 'V'
    derived_units = ['MHz']
    
    def __init__(self, calibration_parameters=None):
        # These parameters are loaded from a globals.h5 type file automatically
        if calibration_parameters is None:
            calibration_parameters = {}
        self.parameters = calibration_parameters
        
        UnitConversion.__init__(self,self.parameters)
        #Left column: voltage 
        #Right column: frequency [MHz]
        self.calib = np.array([[0.00, 49.3],
                               [0.05, 50.5],
                               [0.10, 51.7],
                               [0.15, 52.9],
                               [0.20, 54.0],
                               [0.25, 55.2],
                               [0.30, 56.4],
                               [0.35, 57.6],
                               [0.40, 58.8],
                               [0.45, 59.9]])
        #This calibration is very linear (as expected), so use fitting instead of interpolation.
        self.volts_calib = self.calib[:,0]
        self.freq_calib = self.calib[:,1]
        m, b = np.polyfit(self.volts_calib, self.freq_calib, 1)
        self.volts_to_freq = lambda v: m*v + b
        self.freq_to_volts = lambda f: (f - b)/m

    def MHz_to_base(self, freq):
        return self.freq_to_volts(freq)

    def MHz_from_base(self, volts):
        return self.volts_to_freq(volts)