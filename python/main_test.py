#!/usr/bin/env python3

import sys
import time
import subprocess
import os
from ids import IDS
from gpiozero import Button
from pump_move import PumpMove
from gpiozero import DigitalInputDevice

from config import DATA_DIR, DATA_PREFIX, COMMAND_IDS, ROOT, get_sessioninfo

import argparse

from PumpTest import pump_test

parser=argparse.ArgumentParser()
parser.add_argument('-test',  type=bool, default=False)

args=parser.parse_args()

# get date and time 
datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date=time.strftime("%Y-%m-%d", time.localtime())

# get device and session ids
ids = IDS()
ids.sessionIncrement()

motor_step = ids.step

TEST_SESSION = False


# file to store RFID scann times
RFIDFILE = DATA_DIR + DATA_PREFIX + date + "_" + str(ids.devID)+ "_S"+str(ids.sesID)+ "_RFID.csv"

RatID = input("please scan a command RFID\n")[-8:]


sessioninfo = get_sessioninfo(RatID)

while(len(sessioninfo) == 0):
    RatID = input("command ID not found please rescan the id: ")[-8:]
    sessioninfo = get_sessioninfo(RatID)

    
sessioninfo = sessioninfo[0]


# mover = PumpMove()
# forwardbtn = Button("GPIO5")
# backwardbtn = Button("GPIO27")

# BACKWARD_LIMIT_BTN = "GPIO23"
# BACKWARD_LIMIT = DigitalInputDevice(BACKWARD_LIMIT_BTN)

# def forward():
#     while forwardbtn.value == 1:
#         mover.move("forward")

# def backward():
#     while BACKWARD_LIMIT.value != 1:
#         mover.move("backward")

# forwardbtn.when_pressed = forward
# backwardbtn.when_pressed = backward

if args.test:
    schedule = "fr"
    timeout = 10
    ratio = 10
    sessionLength = 60
else:
    schedule = sessioninfo[0]
    timeout = sessioninfo[1]
    ratio = sessioninfo[2]
    sessionLength = int(sessioninfo[4])


print("Run {} {} for {} hour \n".format(schedule, str(ratio), str(int(sessionLength/3600))))


def scan_rats():
    rat1 = input("please scan rat1\n")[-8:]
    time.sleep(1) # delay for time to get the next rat
    rat2 = input("please scan rat2\n")[-8:]

    while(rat1 == rat2):
        rat2 = input("The IDs of rat1 and rat2 are identical, please scan rat2 again\n")[-8:]

    return rat1, rat2

def record_data(fname, mode ,record):
    with open(fname, mode) as f:
        f.write(record)


file_format = "{}\t{}\t{}\t{}\t{}\n"
def write_header():
    with open(RFIDFILE, "w+") as f:
        f.write(file_format.format("rfid", "time", "act_inact", "lapsed", "poke_count"))


if TEST_SESSION:
    pump_test(motor_step)
else:
    rat1, rat2 = scan_rats()

    print("Session started\nSchedule:{}{}TO{}\nSession Length:{}sec\n",schedule, str(ratio), str(timeout), str(sessionLength))

    # start time
    sTime=time.time()
    lapsed=0

    # delete mover to prevent overheating
    # del(mover)

    subprocess.call("python3 operant_test.py " + \
                    "-schedule " + schedule + \
                    " -ratio " + str(ratio)  + \
                    " -sessionLength " + str(sessionLength) + \
                    " -rat1ID " + str(rat1) + \
                    " -rat2ID " + str(rat2) + \
                    " -timeout " + str(timeout) + \
                    " -rfidFile " + RFIDFILE + \
                    " -devID " + ids.devID + \
                    " -sesID " + str(ids.sesID) + \
                    " &",
                    shell=True
                    )
    # subprocess.call("python3 operant_test.py -schedule {} -ratio {} -sessionLength {} -rat1ID {} -rat2ID {} -timeout {} &".format(schedule, str(ratio), str(sessionLength), rat1, rat2, str(timeout), shell=True))

    poke_counts = {rat1:{"act": 0, "inact": 0}, rat2:{"act":0, "inact":0}}

    write_header()

    while lapsed < sessionLength:
        lapsed=time.time()-sTime
        try:
            rfid=input("rfid waiting\n")
        except EOFError:
            break
        if (len(rfid)==10):
            temp_rfid = rfid[-8:]
            poke_counts[temp_rfid]["inact"] = poke_counts[temp_rfid]["inact"] + 1
            record = file_format.format(temp_rfid, str(time.time()), "inactive", str(lapsed), str(poke_counts[temp_rfid]["inact"]))
            print(record)
            record_data(fname=ROOT+"/_inactive",mode="w+",record=record)
            record_data(fname=RFIDFILE, mode="a+", record=record)
                
        if (len(rfid)==8):
            try:
                poke_counts[rfid]["act"] = poke_counts[rfid]["act"] + 1
            except KeyError as e:
                print("error occured: {}".format(e))

            record = file_format.format(rfid, str(time.time()), "active", str(lapsed), str(poke_counts[rfid]["act"]))
            print(record)
            record_data(fname=ROOT+"/_active",mode="w+",record=record)
            record_data(fname=RFIDFILE,mode="a+", record=record)