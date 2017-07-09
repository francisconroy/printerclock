import printerclock as pc

clkpin = 8
dirpin = 10
enpin = 12

clockstepper = pc.stepperMotor(clkpin, dirpin, enpin)
clockstepper.multistep(100)


