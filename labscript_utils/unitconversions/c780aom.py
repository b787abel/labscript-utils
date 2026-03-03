from .UnitConversionBase import *

class C780AOMConv(UnitConversion):
    base_unit = 'V'
    derived_units = ['relpwr']
    
    def __init__(self, calibration_parameters=None):
        # These parameters are loaded from a globals.h5 type file automatically
        if calibration_parameters is None:
            calibration_parameters = {}
        self.parameters = calibration_parameters
        
        # I[A] = slope * V[V] + shift
        # Saturates at saturation Volts
        
        UnitConversion.__init__(self,self.parameters)
        # We should probably also store some hardware limits here, and use them accordingly 
        # (or maybe load them from a globals file, or specify them in the connection table?)

    def relpwr_to_base(self,amps):
        #here is the calibration code that may use self.parameters
        volts = (amps - 0.1) / 1.0
        return volts
        
    def relpwr_from_base(self,volts):
        amps = 1.0 * volts + 0.1
        return amps 