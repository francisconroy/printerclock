import RPi.GPIO as GPIO

## General config
GPIO.setmode(GPIO.BCM)

# A4988 pins
pin_dict_a4988 = {'dirpin': 4,
            'steppin': 17,
            'sleeppin': 27,
            'resetpin': 22,
            'ms3pin': 18,
            'ms2pin': 25,
            'ms1pin': 24,
            'enpin': 23}
# TB6560 pins
pin_dict_TB6560 = {'dirpin': 16,
            'steppin': 21,
            'enpin': 20}
# door status pins
pin_dict_door_status = {'doorpin': 12}