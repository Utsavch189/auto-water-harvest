import RPi.GPIO as GPIO
import time

class Relay:

    def __init__(self,pin:int):
        self.pin=pin
        self.gpio=GPIO
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.pin,self.gpio.OUT)

    def start(self):
        try:
            self.gpio.output(self.pin,self.gpio.LOW)
        except Exception as e:
            print(e)
            pass

    def stop(self):
        try:
            self.gpio.output(self.pin,self.gpio.HIGH)
        except Exception as e:
            print(e)
            pass

    def clean(self):
        self.gpio.cleanup()

