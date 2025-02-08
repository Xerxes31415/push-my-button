"""

TODO: Find a better way to connect.  It's currently based on short-name, but address would be better.

"""
import board
import struct

# import terminalio
# import displayio
# from adafruit_display_text import label
import time
import digitalio
import random
import pwmio
import array as arr

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

import adafruit_max1704x

from lovense import Lovense

# print(dir(board))

BUTTON_FREQ = 500  # 5 seconds

PWM_MIN = 3000
PWM_MAX = 30000
DUR_MIN = 1000  # 10 seconds
DUR_MAX = 12000  # 120 seconds

stim_int_queue = []
stim_dur_queue = []

pwm = pwmio.PWMOut(board.IO11)
button_led = pwmio.PWMOut(board.IO12)
button_led.duty_cycle = 903
button_led_dir = 1  # 0: down, 1: up
blink_counter = 0

sw = digitalio.DigitalInOut(board.IO10)
sw.direction = digitalio.Direction.INPUT
sw.pull = digitalio.Pull.UP
sw_old = sw.value
sw_counter = 0

# monitor = adafruit_max1704x.MAX17048(board.I2C())
batt_timer = 120

# print(f"Battery voltage: {monitor.cell_voltage:.2f} Volts")

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

toy = None
print("scanning")
found = set()
for entry in ble.start_scan(ProvideServicesAdvertisement, timeout=60, minimum_rssi=-50):
    addr = entry.address
    if addr not in found:
        print(entry)
        if entry.short_name is "LVS-Lush":
            print("Found LUSH")
            toy = ble.connect(entry)
            break
    found.add(addr)

if Lovense in toy:
    print("LVS Service found")
    ctl = toy[Lovense]
    ctl.getBattery()
    ctl.vibe(5)
    

print("scan done")

while True:
    # if switch falling edge is detected, add a new stimulus to the queue
    if sw_old == 0 and sw.value == 1 and sw_counter == 0:
        sw_counter = BUTTON_FREQ
        # Add a new stimulus to the queue

        stim_dur_queue.append(random.randint(DUR_MIN, DUR_MAX))
        stim_int_queue.append(random.randint(PWM_MIN, PWM_MAX))
        print(
            f"Q:[{len(stim_int_queue)}] Intensity: {stim_int_queue[-1]}, Duration: {stim_dur_queue[-1]/100.0}"
        )

    # Limit button presses to BUTTON_FREQ
    if sw_counter > 0:
        sw_counter -= 1
    sw_old = sw.value

    # run the current stimulus in the queue

    if len(stim_int_queue) > 0:
        if stim_dur_queue[0] > 0:
            if stim_dur_queue[0] > 50:
                pwm.duty_cycle = stim_int_queue[0]
            else:
                pwm.duty_cycle = 0
            stim_dur_queue[0] -= 1
        else:
            stim_int_queue.pop(0)
            stim_dur_queue.pop(0)
            print(f"Queue[{len(stim_int_queue)}].")
            if len(stim_int_queue) == 0:
                pwm.duty_cycle = 0
                print("Queue is empty.")
            else:
                print(
                    f"Intensity: {stim_int_queue[0]}, Duration: {stim_dur_queue[0]/100.0}"
                )

    # print("Button LED: ", button_led.duty_cycle)
    if sw_counter > (BUTTON_FREQ - 200):
        if blink_counter < 10:
            button_led.duty_cycle = 65000
        elif blink_counter < 20:
            button_led.duty_cycle = 0
        else:
            blink_counter = 0
        blink_counter += 1
    else:
        if button_led_dir == 1:
            button_led.duty_cycle += 250
            if button_led.duty_cycle >= 45000:
                button_led_dir = 0
        else:  # button_led_dir == 0
            if button_led.duty_cycle > 250:
                button_led.duty_cycle -= 250
            if button_led.duty_cycle <= 600:
                button_led_dir = 1

    batt_timer -= 1
    if batt_timer < 1:
        batt_timer = 120
        #print(f"Battery voltage: {monitor.cell_voltage:.2f} Volts")

    time.sleep(0.01)
