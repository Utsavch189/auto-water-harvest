from relay.relay_module import Relay

class WaterPumpRelay:

    def __init__(self,pin:int,moist_threasold:int=430) -> None:
        self.relay=Relay(pin)
        self.moist_threasold=moist_threasold
        self.relay.stop

    
    def match(self,auto_harvest:bool=None,soil_moist:int=None,pump_start:int=None,pump_end:int=None):
        
        if int(auto_harvest) and soil_moist<self.moist_threasold:
            self.relay.start
        elif not int(auto_harvest):
            self.relay.stop
        
        # pump schedule will be implemented next...
