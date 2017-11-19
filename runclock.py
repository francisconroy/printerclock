import printerclock as pc
import stepmotor as sm
import time

# a4988 breakout PCB
pin_dict = {'dirpin': 4,
            'steppin': 17,
            'sleeppin': 27,
            'resetpin': 22,
            'ms3pin': 18,
            'ms2pin': 25,
            'ms1pin': 24,
            'enpin': 23}

clockstepper = sm.StepperMotorA4988(pin_dict, "A4988", 0, 6800)

while 1:
    h, m, d = pc.gettime()
    pos = pc.getposition(h, m, d)
    clockstepper.gotoposition(pos)
    time.sleep(30)
