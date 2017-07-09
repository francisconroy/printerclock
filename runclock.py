import printerclock as pc
import time

clkpin = 8
dirpin = 10
enpin = 12

clockstepper = pc.stepperMotor(clkpin, dirpin, enpin)

while 1:
    h, m, d = pc.gettime()
    pos = pc.getposition(h, m, d)
    clockstepper.gotoposition(pos)
    time.sleep(30)
