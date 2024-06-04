from relay.relay_module import Relay
from utils import get_current_time

class WaterPumpRelay:

    def __init__(self,pin:int,moist_threasold:int=430) -> None:
        self.relay=Relay(pin)
        self.moist_threasold=moist_threasold
        self.relay.stop

    
    def match(self,auto_harvest:bool=None,soil_moist:int=None,pump_start:int=None,pump_end:int=None,pump_start_now:bool=None):
        print(pump_start_now and (int(pump_start_now)==1))
        print(int(auto_harvest)==1 and soil_moist<self.moist_threasold)
        print(pump_start and pump_end and (pump_start>=get_current_time() and pump_end<=get_current_time()))
        
        if pump_start_now and (int(pump_start_now)==1):
            self.relay.start
            return
    
        if int(auto_harvest)==1 and soil_moist<self.moist_threasold:
            self.relay.start
            return    
        
        if pump_start and pump_end and (pump_start>=get_current_time() and pump_end<=get_current_time()):
            self.relay.start
            return
        
        
        self.relay.stop

        
        

