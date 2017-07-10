import printerclock as pc
import time

clkpin = 12
dirpin = 16
enpin = 18

clockstepper = pc.stepperMotor(clkpin, dirpin, enpin)

while 1:
    h, m, d = pc.gettime()
    pos = pc.getposition(h, m, d)
    clockstepper.gotoposition(pos)
    time.sleep(30)
