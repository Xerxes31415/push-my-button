'''
Lovense Driver

TODO: Make the UUID dynamic
TODO: Flesh out the functions
'''
from adafruit_ble.services import Service
from adafruit_ble.uuid import VendorUUID
from adafruit_ble.characteristics.stream import StreamOut, StreamIn
from adafruit_ble.characteristics.string import StringCharacteristic
from adafruit_ble.characteristics import Characteristic
import time

class Lovense(Service):
    uuid = VendorUUID("53300001-0023-4bd4-bbd5-a6920e4c5653")
    _out = StringCharacteristic(uuid = VendorUUID("53300002-0023-4bd4-bbd5-a6920e4c5653"), properties=Characteristic.WRITE)
    _response = StreamIn(uuid = VendorUUID("53300003-0023-4bd4-bbd5-a6920e4c5653"), properties=Characteristic.NOTIFY)
    #_out = StreamIn(uuid = VendorUUID("53300002-0023-4bd4-bbd5-a6920e4c5653"))
    #_response = StreamOut(uuid = VendorUUID("53300003-0023-4bd4-bbd5-a6920e4c5653"))

    def getBattery(self) -> int:
        print("fetching Batt")
        self._out = "Battery;"
        time.sleep(1)
        #print("Battery = " + self.response)
        return 0

    def vibe(self, val: int):
        self._out = "Vibrate:10;"
        time.sleep(1)
        self._out = "Vibrate:0;"

    def status(self)->int:
        return 0
    def powerOff(self):
        pass
        
    def getDeviceInfo(self)->str:
        return "TBD"

    # TODO: Light and LED functions
    # TODO: Auto Resume settings
    # TODO: Accelerometer Data
    # TODO: Rotation Speed and Direction
    # TODO: Air Levels
    # TODO: Programmed Patterns
    # TODO: Other House Keeping functions