# PeerPub 
 Tracking two rats independently during oral operant self-administration of solutions (e.g. sucrose, alcohol, opioids).

## Program Structure

    Main Program: main.py (main_test.py) is the entry program. This program handles session command and rat ID
    scanning, adjusting the pump position, and finally calling the operant.py as a subprocess.
    Note that this program does not exit after calling the subprocess. It it kept alive, as the
    main thread, to record rat's ID when they poke their head near the antenna. Rat's ID are
    stored in _active and _inactive files located in the /home/pi/ directory.
    
    Operant Program: operant.py (operant_test.py) is the program which main invoke at the end of it's executation.
    This program handles saving each data point to corresponding data files.
    

## Configuration
   - Files

     - /home/pi/peerpub_config.json
        This file stores 3 information: device ID, session number/ID, and stepper motor step size. (The session number is increament by 1 each time the program start)

     - /home/pi/openbehavior/PeerPub/python/session_configuration.csv
        This file is used by the program to read in the session information. 

     - /home/pi/openbehavior/PeerPub/python/config.py
        This file stores different directory paths. Note that these path are all absolute paths. There's a "get_sessioninfo" function which takes in a argument "sessionid" to retrive session information from "session_configuration.csv" mentioned above. A good practice is to put related configuration functions in this file and import then when needed.

## Utility Scripts

    **check_empty_program.sh**: a script that check the size of every python file in the python/ directory. If one or more files are empty the script then reclone the entire repository.