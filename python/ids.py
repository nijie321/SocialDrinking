#!/usr/bin/python3 


import os
import time

from config import ROOT
import json

import sys


DEVID_FILE = ROOT+'/deviceid'
RATID_FILE = ROOT+'/ratids'
SESSIONID_FILE = ROOT+'/sessionid'

JSON_CONFIG_FILE = ROOT + '/peerpub_config.json'

class IDS:
    def __init__(self):
        try:
            with open(JSON_CONFIG_FILE ,'r') as f:
                json_data = json.load(f)
        except FileExistsError:
            sys.exit("peerpub_config.json file not found in /home/pi")
            
        self.devID = json_data['deviceid']
        self.sesID = json_data['sessionid']
        self.step = json_data['step']
    def sessionIncrement(self):
        f = open(JSON_CONFIG_FILE, 'w')
        
        json.dump({
            "deviceid": self.devID,
            "step": self.step,
            "sessionid": self.sesID + 1
        }, f)

        f.close()