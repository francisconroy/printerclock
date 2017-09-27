import printerclock as pc
import RPi.GPIO as GPIO

# a4988 breakout PCB
pin_dict = {'dirpin': 4,
            'steppin': 17,
            'sleeppin': 27,
            'resetpin': 22,
            'ms3pin': 18,
            'ms2pin': 25,
            'ms1pin': 24,
            'enpin': 23}

clockstepper = pc.stepperMotorA4988(pin_dict)

GPIO.output(pin_dict['steppin'], GPIO.HIGH) # for current measurement