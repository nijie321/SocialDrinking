#!/usr/bin/env python3

import sys
import time
import subprocess
import os
from ids import *
from gpiozero import Button
from pump_move import PumpMove
from gpiozero import DigitalInputDevice

import traceback
import logging


from PumpTest import pump_test

# logger
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

# handler (output all log to a file and if the log is error, also output to console)
fh = logging.FileHandler('/home/pi/main.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add handlers
logger.addHandler(fh)
logger.addHandler(ch)



# get date and time 
datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
date=time.strftime("%Y-%m-%d", time.localtime())
# get device and session ids
ids = IDS()
ids.sessionIncrement()
# file to store RFID scann times
try:
    RFIDFILE=DATA_DIR + DATA_PREFIX + date + "_" + str(ids.devID)+ "_S"+str(ids.sesID)+ "_RFID.csv"
except:
    logger.exception("don't know what kind of exception")
    # logger.exception("error %s", e)

RatID=input("please scan a command RFID\n")[-8:]


command_ids = [
    "0084cb3c",
    "002cd652",
    "002ba76f",
    "002c7365",
    "002c94ef",
    "002ceeb8",
    "0087739a",
    "002d54ff",
    "0084668e",
    "002cd488",
    "002cbc8f",
    "002b51b9",
    "002d558c",
    "002d3da7",
    "002b397e",
    "002c732f",
    "002b392d",
    "002cdfc3",
    "00871805",
    
    # test ID
    "0084c36b",
    "008773ba",

    # fr5timeout10
    "002c1aa3",
    "002ce87b"
]

TEST_SESSION = False

while RatID not in command_ids:
    RatID = input("command ID not found, please rescan the id: ")[-8:]

# the default schedule is vr10 timeout10. Other reinforcemnt schedules can be started by using RFIDs.
if RatID[-2:] == "3c" or RatID[-2:] == "88": # PR
    schedule="pr"
    breakpoint=2
    timeout = 10
    nextratio=int(5*2.72**(breakpoint/5)-5)
    sessionLength=20*60 # session ends after 20 min inactivity
    ratio=""
    #signal motion sensor to keep recording until this is changed
    with open ("ROOT/prend", "w") as f:
        f.write("no")
elif RatID[-2:] == "7b" or RatID[-2:] == "a3": # FR5 30min
    schedule="fr"
    ratio = 5
    timeout = 10
    sessionLength = 60 * 30
    nextratio = ratio
elif RatID[-2:] == "52" or RatID[-2:] == "8f":  #FR5 1h
    schedule="fr"
    ratio = 5
    timeout =  10
    sessionLength=60*60*1 # one hour assay
    nextratio=ratio
elif RatID[-2:] == "05" or RatID[-2:] == "c4":  #FR5 4h
    schedule="fr"
    ratio = 5
    timeout =  10
    sessionLength=60*60*4 # four hour assay
    nextratio=ratio
elif RatID[-2:] == "6f" or RatID[-2:] == "b9": # FR5, 16h 
    schedule="fr"
    ratio = 5
    timeout =  10
    sessionLength=60*60*16 # one hour assay
    nextratio=ratio
elif RatID[-2:] == "65" or RatID[-2:] == "8c": # extinction
    schedule="ext"
    timeout=0
    ratio=1000000
    nextratio=1000000
    sessionLength=60*60*1
elif RatID[-2:] == "ef" or RatID[-2:] == "a7": #VR10, 1h
    schedule="vr"
    ratio = 10
    timeout =  10
    sessionLength=60*60*1 #
    nextratio=ratio
elif RatID[-2:] == "b8" or RatID[-2:] == "7e": #VR10, 2h
    schedule="vr"
    ratio = 10
    timeout =  10
    sessionLength=60*60*2 #
    nextratio=ratio
elif RatID[-2:] == "9a" or RatID[-2:] == "2f": #VR10, 4h
    schedule="vr"
    ratio = 10
    timeout =  10
    sessionLength=60*60*4 #
    nextratio=ratio
elif RatID[-2:] == "ff" or RatID[-2:] == "2d": #VRreinstate, 4h
    vreinstate=1
    schedule="vr"
    ratio = 5
    timeout = 1
    sessionLength=60*60*4 # one hour assay
    nextratio=ratio
    RatID=ReadRFID("/dev/ttyAMA0")
elif RatID[-2:] == "8e" or RatID[-2:] == "c3": # vr10 16h
    schedule="vr"
    ratio=10
    nextratio=ratio
    timeout = 10
    sessionLength=60*60*16
elif RatID[-2:] == "6b" or RatID[-2:] == "ba":
    TEST_SESSION = True
    
    

if TEST_SESSION:
    pump_test()
else:
    # 20ML motor step
    motor_step = ""
    with open(MOTOR_STEP_FILE, 'r') as f:
        motor_step = f.read().strip()
        print(motor_step)

#### PUMP and BUTTON
# start the pump after the command ID is scanned
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


    h=str(int(sessionLength/3600))
    sep="===================================\n  "
    print(sep+datetime+"\n"+sep)
    print("Run " + schedule + str(ratio) + "for "  + h + "h\n")

    rat1 = input("please scan rat1\n")[-8:]
    time.sleep(1) # delay for time to get the next rat
    rat2 = input("please scan rat2\n")[-8:]

    while(rat1 == rat2):
        rat2 = input("The IDs of rat1 and rat2 are identical, please scan rat2 again\n")[-8:]

    print("Session started\nSchedule:"+schedule+str(ratio)+"TO"+str(timeout)+"\nSession Length:"+str(sessionLength)+"sec\n")
# start time
    sTime=time.time()
    lapsed=0

# delete mover to prevent overheating
    del(mover)

    subprocess.call("python3 operant.py -schedule " +schedule+ " -ratio " +str(ratio)+ " -sessionLength " + str(sessionLength) + " -rat1ID " + rat1 + " -rat2ID " + rat2 + " -timeout " + str(timeout) + " -motorStep " + motor_step +  " & ", shell=True)

    poke_counts = {rat1:{"act": 0, "inact": 0}, rat2:{"act":0, "inact":0}}

    while lapsed < sessionLength:
        lapsed=time.time()-sTime
        try:
            rfid=input("rfid waiting\n")
        except EOFError:
            # when the input encounter the end of line before reading any input
            continue
        try:
            if (len(rfid)==10):
                temp_rfid = rfid[-8:]
                poke_counts[temp_rfid]["inact"] = poke_counts[temp_rfid]["inact"] + 1
                record=temp_rfid+"\t"+str(time.time())+ "\tinactive\t" + str(lapsed) +"\n"
                with open(ROOT + "/_inactive", "w+") as inactive:
                    inactive.write(record)
                    inactive.close()
                with open(RFIDFILE, "a+") as inactive:
                    print ("\n    inactive spout " + temp_rfid + "\t")
                    inactive.write(record)
                fname = "{}/{}_inact_count.txt".format(DATA_DIR, temp_rfid)
                with open(fname, "w+") as f:
                    f.write("{}:{}".format(temp_rfid, poke_counts[temp_rfid]["inact"]))
                    

            if (len(rfid)==8):
                try:
                    poke_counts[rfid]["act"] = poke_counts[rfid]["act"] + 1
                except KeyError as e:
                    with open(ROOT + "/error.log", "a+") as f:
                        f.write("error - {}\n".format(e))
                        f.write("poke_counts - {}\n".format(poke_counts))
                        f.write("rfid - {}\n".format(rfid))

                record=rfid+"\t"+str(time.time())+ "\tactive\t" + str(lapsed)+ "\n"
                with open(ROOT+"/_active", "w+") as active:
                    active.write(record)
                    active.close()
                with open(RFIDFILE, "a+") as active:
                    print ("\n      active spout " + rfid + "\t")
                    active.write(record)
                fname = "{}/{}_act_count.txt".format(DATA_DIR, rfid)
                with open(fname, "w+") as f:
                    f.write("{}:{}".format(rfid,poke_counts[rfid]["act"]))
        except KeyError as ke:
            pass
            
            
        except OSError as oe:
            pass

            
        except:
            pass

            
