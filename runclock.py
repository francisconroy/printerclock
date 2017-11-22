import printerclock as pc
import stepmotor as sm
import time
import nymph_pins as np


clockstepper = sm.StepperMotorA4988(np.pin_dict_a4988, sm.StepperMotorA4988.type, 0, 6800)

while 1:
    h, m, d = pc.gettime()
    pos = pc.getposition(h, m, d)
    clockstepper.gotoposition(pos)
    time.sleep(30)
