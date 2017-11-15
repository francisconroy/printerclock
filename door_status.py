import RPi.GPIO as GPIO


def check_door_status(pindict):
    return GPIO.input(pindict['doorpin'])

pin_dict = {'doorpin': 12}
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_dict['doorpin'], GPIO.IN)

while(1):
    print(check_door_status(pin_dict))