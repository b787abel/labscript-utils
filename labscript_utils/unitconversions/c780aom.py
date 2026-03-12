from .UnitConversionBase import *
from scipy.interpolate import interp1d
import numpy as np 

class C780AOMConv(UnitConversion):
    base_unit = 'V'
    derived_units = ['relpwr']
    
    def __init__(self, calibration_parameters=None):
        # These parameters are loaded from a globals.h5 type file automatically
        if calibration_parameters is None:
            calibration_parameters = {}
        self.parameters = calibration_parameters
        
        UnitConversion.__init__(self,self.parameters)
        #Left column: voltage 
        #Right column: optical power 
        self.calib = np.array([[-0.25, 0.8],
                               [-0.20, 4.3],
                               [-0.15, 12.2],
                               [-0.10, 24.2],
                               [-0.05, 40.2],
                               [0.0,   60],
                               [0.05,  82],
                               [0.10,  107],
                               [0.15,  133],
                               [0.20,  159],
                               [0.25,  187],
                               [0.3,   217],
                               [0.35,  240],
                               [0.4,   263],
                               [0.45,  285],
                               [0.5,   303],
                               [0.55,  319],
                               [0.6,   330],
                               [0.65,  339], 
                               [0.7,   399]])
        self.volts_calib = self.calib[:,0]
        self.pwr_calib = self.calib[:,1]/np.max(self.calib[:,1]) # normalise to 1.0 at max power

        self.volts_to_rel_pwr = interp1d(self.volts_calib, self.pwr_calib, bounds_error=False, fill_value=(0,1))
        self.rel_pwr_to_volts = interp1d(self.pwr_calib, self.volts_calib, bounds_error=False, fill_value=(self.volts_calib[0], self.volts_calib[-1]))
        # We should probably also store some hardware limits here, and use them accordingly 
        # (or maybe load them from a globals file, or specify them in the connection table?)

    def relpwr_to_base(self,relpwr):
        return self.rel_pwr_to_volts(relpwr)
        
    def relpwr_from_base(self,volts):
        return self.volts_to_rel_pwr(volts)