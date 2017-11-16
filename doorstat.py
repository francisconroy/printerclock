import RPi.GPIO as GPIO

## Door checker
def check_door_status(pindict):
    return GPIO.input(pindict['doorpin'])