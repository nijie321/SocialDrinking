
# HOUSE LIGHTS
# houselight_on = False
# def houselight_check(houselight_on):
#     # global houselight_on
#     blink_light_command = "sudo python ./blinkenlights.py &"
#     if not FORWARD_LIMIT_REACHED:
#         if (time.localtime().tm_hour >= 21 and houselight_on is False) or (time.localtime().tm_hour >= 9 and time.localtime().tm_hour < 21) and houselight_on:
#             houselight_on = True
#             subprocess.call(blink_light_command, shell=True)


# RATID
def get_ratid_scantime(rats, fname, this_lick, act, maxILI, maxISI):
    try:
        with open(fname, "r") as f:
            rat, scantime, *dummies = f.read().strip().split("\t")
            scantime = float(scantime)
            
    except (OSError, ValueError) as e:
        # logging.exception("ratid error: %s", e)
        rat = "ratUnknown"
        scantime = 0

    try:
        if rat is None:
            rat = "ratUnknown"
        else:
            rat_obj = rats[rat]
            if act:
                last_lick = rat_obj.last_act_licks["time"]
            else:
                last_lick = rat_obj.last_inact_licks["time"]
            
            if this_lick - last_lick > maxILI and this_lick - scantime > maxISI:
                rat = "ratUnknown"
            
    except KeyError:
        print("error from get_ratid_scantime")

    return rat, scantime


# SYRINGE
def reload_syringe():
    from pump_move import PumpMove
    from gpiozero import DigitalInputDevice

    BACKWARD_LIMIT = DigitalInputDevice("GPIO23")
    def backward():
        while BACKWARD_LIMIT.value != 1:
            mover.move("backward")
    
    mover = PumpMove()
    while BACKWARD_LIMIT.value != 1:
        mover.move("backward")
    del(mover)
