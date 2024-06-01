import adafruit_dht

class DHT11Sensor:

    def __init__(self,board_pin) -> None:
        try:
            self.dht_device = adafruit_dht.DHT11(board_pin)
        except:
            self.dht_device=None
    
    @property
    def getTemp(self):
        try:
            return self.dht_device.temperature
        except Exception as e:
            return None
    
    @property
    def getHumidity(self):
        try:
            return self.dht_device.humidity
        except Exception as e:
            return None



if __name__=="__main__":
    import board
    dht=DHT11Sensor(board_pin=board.D17)
    print(dht.getHumidity,"  ",dht.getTemp)