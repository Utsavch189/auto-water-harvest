from relay.relay_module import Relay
from utils import get_current_time

class WaterPumpRelay:

    def __init__(self,pin:int,moist_threasold:int=430) -> None:
        try:
            self.relay=Relay(pin)
            self.moist_threasold=moist_threasold
            self.relay.stop
        except Exception as e:
            print(e)

    
    def match(self,auto_harvest:bool=None,soil_moist:int=None,pump_start:int=None,pump_end:int=None,pump_start_now:bool=None):
        try:

            if pump_start_now and (int(pump_start_now)==1):
                self.relay.start
                return

            if int(auto_harvest)==1 and soil_moist<self.moist_threasold:
                self.relay.start
                return    

            if pump_start!="00:00:00" and pump_end!="00:00:00" and (get_current_time()>=pump_start and get_current_time()<=pump_end):
                self.relay.start
                return

            self.relay.stop

        except Exception as e:
            print(e)

        
        

