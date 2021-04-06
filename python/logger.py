
# import BASE_DIR from config
# from config import BASE_DIR
# print(BASE_DIR)


# class Logger():
#     def __init__(self,file_name):
#         self.file_name = file_name
#         self.data_str = ""

#     def write_data_str(self, data):
#         self.data_str += "{}{}".format(data, "\n")
        
    
#     def save_file(self):
#         with open(self.file_name, "a+") as f:
#             f.write(self.data_str)
            
        
        

import time
import string
from config import DATA_DIR, DATA_PREFIX

class LickLogger:
    def __init__(self, devID, sesID):
        self.devID = devID
        self.sessID= sesID
        self.startTime=time.strftime("%Y-%m-%d\t%H:%M:%S", time.localtime())
        # self.data_str = ""
        self.data_format = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n"
        

    def createDataFile(self, schedule, ratIDs):
        date=time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        self.datafile = DATA_DIR + "/" +  DATA_PREFIX + "_" + date + "_" + str(self.devID) + '_S' + str(self.sessID) +  "_" + schedule + "_" + str(ratIDs) + '.csv'
        print ("\nData file location:\n", self.datafile)

        # write header to data file
        with open(self.datafile,"a") as f:
            f.write(self.data_format.format("rat_id", "rfidSec", "date", "start_time", "boxid", "event_type", schedule, "lapsedSec"))

    def logEvent(self, rat, eventSec, eventType, timeLapsed, ratio=0):
        # Create output string
        outputstr = rat + "\t" + str(eventSec) + "\t"+ time.strftime("%Y-%m-%d\t%H:%M:%S", time.localtime()) + "\t" + self.devID + "_S" + str(self.sessID) + "\t" + eventType + "\t" + str(ratio) + "\t"+ str(timeLapsed) + "\n"
        # self.data_str += outputstr
        print (outputstr)
        with open (self.datafile, "a") as datafile:
            datafile.write(outputstr)

    # def save_data(self):
    #     with open(self.datafile, "a") as f:
    #         f.write(self.data_str)
        
    @staticmethod
    def finalLog(fname,data_dict):
        ratids = [data_dict["ratID1"][0], data_dict["ratID2"][0]]
        poke_counts = {ratids[0]:{"act":0, "inact": 0}, ratids[1]:{"act":0, "inact":0}}
        poke_count_files = {"ACT_POKE": ["{}_act_count.txt".format(ID) for ID in ratids],
                            "INACT_POKE": ["{}_inact_count.txt".format(ID) for ID in ratids]
                           }

        with open(DATA_DIR + "/" + fname, "a+") as f:
            for ref, count_files in poke_count_files.items():
                for file in count_files:
                    try:
                        with open(DATA_DIR + "/" + file, "r") as f1:
                            (rfid,poke_count) = f1.read().split(":")
                            if ref == "ACT_POKE":
                                poke_counts[rfid]["act"] = poke_count
                            else:
                                poke_counts[rfid]["inact"] = poke_count
                    except FileNotFoundError:
                        continue

        with open(DATA_DIR+ "/" + fname, "a+") as f:
            ID1_str = (("{}\t"*11).format(*data_dict["ratID1"], *poke_counts[ratids[0]].values())) + "\n"
            ID2_str = (("{}\t"*11).format(*data_dict["ratID2"], *poke_counts[ratids[1]].values())) + "\n"
            ID0_str = (("{}\t"*9).format(*data_dict["ratID0"])) + "\n"
            f.write(ID1_str + ID2_str + ID0_str)
        