import RPi.GPIO as GPIO

class DoorStat(object):
    def __init__(self, pin_dict):
        self.pindict = pin_dict
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_dict['doorpin'], GPIO.IN)

    ## Door checker
    def check_door_status(self):
        return GPIO.input(self.pindict['doorpin'])
