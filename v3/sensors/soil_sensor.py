import busio,board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class SoilSensor:
    
    def __init__(self) -> None:
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.ads = ADS.ADS1115(i2c)
        except Exception as e:
            self.ads=None
            print(e)

    @property
    def getMoisture(self):
        try:
            chan = AnalogIn(self.ads, ADS.P0)
            moist=chan.value
            voltage=chan.voltage
            return moist,voltage
        except Exception as e:
            print(e)
            return None

if __name__=="__main__":
    s=SoilSensor()
    print(s.getMoisture)