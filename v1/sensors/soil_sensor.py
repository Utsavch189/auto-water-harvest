import busio,board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class SoilSensor:
    
    def __init__(self) -> None:
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(i2c)

    @property
    def getMoisture(self):
        chan = AnalogIn(self.ads, ADS.P0)
        moist=chan.value
        voltage=chan.voltage
        return moist,voltage

if __name__=="__main__":
    s=SoilSensor()
    print(s.getMoisture)