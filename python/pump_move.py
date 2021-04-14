from time import sleep
import RPi.GPIO as GPIO
# import argparse
import signal
import sys
from gpiozero import InputDevice
from gpiozero import Servo
import pigpio
# from gpiozero import DigitalInputDevice
# from gpiozero import SmoothedInputDevice

steps=150
rotate_dir=1

GPIO.setwarnings(False)

class PumpMove:
    def __init__(self):
        self.DIR = 26
        self.STEP = 6
        self.CW = 1
        self.CCW = 0
        self.SLEEP = 25

        # self.pi = pigpio.pi()
        # self.pi.set_mode(self.DIR, pigpio.OUTPUT)
        # self.pi.set_mode(self.STEP, pigpio.OUTPUT)
        # self.pi.set_mode(self.SLEEP, pigpio.OUTPUT)
        
        self.GPIO = GPIO
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setup(self.DIR, self.GPIO.OUT, initial=self.GPIO.HIGH)
        # self.GPIO.setup(self.SLEEP, self.GPIO.OUT, initial=self.GPIO.LOW)
        self.GPIO.setup(self.STEP, self.GPIO.OUT, initial=self.GPIO.HIGH)
        self.GPIO.output(self.DIR,self.CW)
        

        self.MODE = (17,22)
        self.GPIO.setup(self.MODE, self.GPIO.OUT)

        self.RESOLUTION = {
                            'Full': (0,0),
                            'Half': (1,0),
                            '1/8': (0,1),
                            '1/16': (1,1),
                          }
        
        self.step_counts = steps
        self.delay = .0209 / 50
        # self.delay = 0.005
        self.rotate_dir = rotate_dir

        # self.pi.set_PWM_dutycycle(self.STEP, 128)
        # self.pi.set_PWM_frequency(self.STEP, 500)
        

    def move(self, direction, steps=150):
        # self.pi.write(self.SLEEP, 1)
        direction_dict = {"forward": self.CW, "backward": self.CCW}

        # for i in range(2):
        #     self.pi.write(self.MODE[i], self.RESOLUTION['Full'][i])

        # for i in range(steps):
        #     self.pi.write(self.DIR, direction_dict[direction])
            # sleep(self.delay)

        try:
            # self.GPIO.output(self.SLEEP, self.GPIO.HIGH)
            self.GPIO.output(self.MODE, self.RESOLUTION['Full'])
            self.GPIO.output(self.DIR, direction_dict[direction])

            for step in range(steps):
                self.GPIO.output(self.STEP, self.GPIO.HIGH)
                sleep(self.delay)
                self.GPIO.output(self.STEP, self.GPIO.LOW)
                sleep(self.delay)

            self.GPIO.output(self.STEP, self.GPIO.HIGH)
        except KeyError:
            print("please enter a correct direction")
        
        # self.pi.write(self.SLEEP, 0)

    def __del__(self):
        # self.GPIO.output(self.SLEEP, self.GPIO.LOW)
        self.GPIO.cleanup(self.MODE)
        # self.pi.set_PWM_dutycycle(self.STEP, 0)
        # self.pi.write(self.SLEEP, 0)
        # self.pi.stop()
