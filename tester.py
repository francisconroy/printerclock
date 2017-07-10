import printerclock as pc

clkpin = 12
dirpin = 16
enpin = 18

clockstepper = pc.stepperMotor(clkpin, dirpin, enpin)
clockstepper.multistep(100)


