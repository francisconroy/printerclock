import RPi.GPIO as GPIO


def do_init(pin_dict):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_dict['doorpin'], GPIO.IN)

## Door checker
def check_door_status(pindict):
    return GPIO.input(pindict['doorpin'])