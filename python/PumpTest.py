
from gpiozero import Button
from gpiozero import DigitalInputDevice
from pump_move import PumpMove

import board
import busio
import adafruit_mpr121

import time

# import RPi.GPIO as gpio
# gpio.setwarnings(False)
# gpio.setmode(gpio.BCM)

def pump_test(step_size):

    # command = input("Please scan the ") 
    act_count = 0
    i2c = busio.I2C(board.SCL, board.SDA)
    mpr121 = adafruit_mpr121.MPR121(i2c)

    mover = PumpMove()
    forwardbtn = Button("GPIO5")
    backwardbtn = Button("GPIO27")

    BACKWARD_LIMIT_BTN = "GPIO23"
    BACKWARD_LIMIT = DigitalInputDevice(BACKWARD_LIMIT_BTN)

    def forward():
        while forwardbtn.value == 1:
            mover.move("forward")

    def backward():
        while BACKWARD_LIMIT.value != 1:
            mover.move("backward")

    forwardbtn.when_pressed = forward
    backwardbtn.when_pressed = backward

    
    while True:
        time.sleep(0.050) # allow 20 licks per sec
        act = mpr121.touched_pins[1]
        if act:
            print("act_count = ", act_count)
            if act_count % 5 == 0:
                for i in range(5):
                    mover.move("forward", step_size)
                    print("step = ", step_size)
                act_count = 0
            act_count += 1