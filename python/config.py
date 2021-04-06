

BASE_DIR = "./SocialDrink"


ROOT = "/home/pi"
DATA_DIR = "{}/{}/".format(ROOT, "SocialDrinking")
DATA_PREFIX = "Soc"

CONFIG_FILE = "session_configuration.csv"

def get_sessioninfo(sessionid):
    with open(CONFIG_FILE, "r") as f:
        csv_data = f.read().split("\n")
        
    sessioninfo = [info.split(",")[2:] for info in csv_data[1:] if sessionid in info.split(",")[:2]]

    return sessioninfo
    # if len(sessioninfo) < 1:
    #     raise IndexError
    # else:
    #     return sessioninfo[0]
    

COMMAND_IDS = [
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

    # test ID
    "0084c36b",
    "008773ba",

    # fr5timeout10
    "002c1aa3",
    "002ce87b",
]
