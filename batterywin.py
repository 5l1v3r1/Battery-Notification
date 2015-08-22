__author__ = 'Saumyakanta Sahoo'

from ctypes import *

class PowerClass(Structure):
    _fields_ = [('ACLineStatus', c_byte),
            ('BatteryFlag', c_byte),
            ('BatteryLifePercent', c_byte),
            ('Reserved1',c_byte),
            ('BatteryLifeTime',c_ulong),
            ('BatteryFullLifeTime',c_ulong)]    

powerclass = PowerClass()
result = windll.kernel32.GetSystemPowerStatus(byref(powerclass))

#print(powerclass.BatteryLifePercent)

