# Write your code here :-)
import time
import re


from adafruit_ble.services import Service
from adafruit_ble.uuid import *
from adafruit_ble.characteristics.stream import StreamOut, StreamIn
from adafruit_ble.characteristics.string import StringCharacteristic
from adafruit_ble.characteristics import Characteristic

from lovenseUARTService import LovenseUARTService

class Lovense(LovenseUARTService):

    def __init__(self, service: None, uuid: VendorUUID=None) -> None:
        super().__init__(service=service)

    """ -----------------------------------------------------------------------------"""

    def vibrate(self, intensity: int):
        if intensity < 0:
            intensity =0
        if intensity >20:
            intensity = 20
        self.write(f'Vibrate:{intensity};')
        #print(self.read(3).decode())

    def getBattery(self) -> int:
        self.reset_input_buffer()
        print("fetching Batt")
        self.write("Battery;")
        time.sleep(0.1)
        print("Battery = " + self.read(50).decode())
        return 0

    """ ---------------------------------------Added Functions--------------------------------------"""

    def connection_alert(self):
        print("Connection Alert")
        for intensity in [5,10,15,20]:
            self.vibrate(intensity)
            time.sleep(0.4)
            self.vibrate(0)
            time.sleep(0.6)

