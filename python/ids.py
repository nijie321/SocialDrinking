#!/usr/bin/python3 


import os
import time

from config import ROOT

DEVID_FILE = ROOT+'/deviceid'
RATID_FILE = ROOT+'/ratids'
SESSIONID_FILE = ROOT+'/sessionid'

class IDS:
    def __init__(self):
        with open (DEVID_FILE) as devID:
            self.devID = str((devID.read()).strip())
            devID.close()
        with open (SESSIONID_FILE, "r") as sessID:
            self.sesID=int(sessID.read().strip())
            #newSesID=self.sesID+1
            #sessID.seek(0)
            #sessID.write(str(newSesID))
            #sessID.close()
    def sessionIncrement(self):
        with open (SESSIONID_FILE, "r+") as sessID:
            self.sesID=int(sessID.read().strip())
            newSesID=self.sesID+1
            self.sesID = newSesID
            sessID.seek(0)
            sessID.write(str(newSesID))
            

