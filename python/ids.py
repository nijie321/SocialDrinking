#!/usr/bin/python3 


import os
import time

from config import ROOT
import json


DEVID_FILE = ROOT+'/deviceid'
RATID_FILE = ROOT+'/ratids'
SESSIONID_FILE = ROOT+'/sessionid'

JSON_CONFIG_FILE = ROOT + '/peerpub_config.json'


class IDS:
    def __init__(self):
        with open(JSON_CONFIG_FILE ,'r') as f:
            json_data = json.load(f)
        self.devID = json_data['deviceid']
        self.sesID = json_data['sessionid']
        self.step = json_data['step']

        # with open (DEVID_FILE) as devID:
        #     self.devID = str((devID.read()).strip())
        #     devID.close()
        # with open (SESSIONID_FILE, "r") as sessID:
        #     self.sesID=int(sessID.read().strip())

            #newSesID=self.sesID+1
            #sessID.seek(0)
            #sessID.write(str(newSesID))
            #sessID.close()
    def sessionIncrement(self):
        f = open(JSON_CONFIG_FILE, 'r')
        
        json.dump({
            "deviceid": self.devID,
            "step": self.step,
            "sessionid": self.sesID + 1
        }, f)

        f.close()

        # with open (SESSIONID_FILE, "r+") as sessID:
        #     self.sesID=int(sessID.read().strip())
        #     newSesID=self.sesID+1
        #     self.sesID = newSesID
        #     sessID.seek(0)
        #     sessID.write(str(newSesID))
            

