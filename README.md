# SocialDrinking
 
 Tracking two rats independently during oral operant self-administration of solutions (e.g. sucrose, alcohol, opioids).


## Configuration
   - Files

     - /home/pi/peerpub_config.json
        This file stores 3 information: device ID, session number/ID, and stepper motor step size. (The session number is increament by 1 each time the program start)

     - /home/pi/openbehavior/PeerPub/python/session_configuration.csv
        This file is used by the program to read in the session information. 

     - /home/pi/openbehavior/PeerPub/python/config.py
        This file stores different directory paths. Note that these path are all absolute paths. There's a "get_sessioninfo" function which takes in a argument "sessionid" to retrive session information from "session_configuration.csv" mentioned above. A good practice is to put related configuration functions in this file and import then when needed.
