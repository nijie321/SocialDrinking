
from gpiozero import Button
from gpiozero import DigitalInputDevice
from pump_move import PumpMove
import board
import busio
import adafruit_mpr121
from ids import IDS
import time

file_dir = "/home/pi/SocialDrinking/{}"


def pump_calibration(step_size, fname):
    old_step = step_size
    step = step_size
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

    print("current step size = " + str(step_size)) 
    print("please prepare to measure the solution.")

    while True:
        time.sleep(0.050)
        act = mpr121.touched_pins[1]

        if act:
            if act_count % 5 == 0:
                for i in range(5):
                    mover.move("forward", step)

            act_count += 1

            if act_count == 15:
                response = input("please enter the amount measured (numeric value) or scan the command id again to exit: ").strip()
                if response[-2:] == '16' or response[-2:] == '89' or response[-2:] == 'ba':
                    break
                else:
                    try:
                        response = int(response)
                    except ValueError:
                        response = int(input("please re-enter the amount measured: ").strip())

                avg_measured_value = response / 3
                print("average value: {}".format(avg_measured_value))
                
                if (avg_measured_value < (300-10) and avg_measured_value > (300+10)):
                    # update step size
                    print("previous step: {}".format(step))
                    step = ( (step*5 / 300) * avg_measured_value )  / 5
                    print("modified step: {}".format(step))
                
                act_count = 0

    date = time.strftime("%Y-%m-%d", time.localtime())
    d_time = time.strftime("%Y-%m-%d", time.localtime())
    record = "{}\t"*4

    ids = IDS()
    print("old step size: {}".format(old_step))
    print("new step size: {}".format(step))
    ids.change_step(step)

    try:
        with open(file_dir.format(fname), "w") as f:
            f.write(record.format(date, d_time, old_step, step))
    except FileNotFoundError:
        f = open(file_dir.format(fname), "x")
        f.close()
        with open(file_dir.format(fname), "w") as f:
            f.write(record.format(date, d_time, old_step, step))
    finally:
        del(mover)

