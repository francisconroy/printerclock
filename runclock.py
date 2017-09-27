import printerclock as pc
import time

clkpin = 12
dirpin = 16
enpin = 18
sleeppin = 11


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

while 1:
    h, m, d = pc.gettime()
    pos = pc.getposition(h, m, d)
    clockstepper.gotoposition(pos)
    time.sleep(30)
