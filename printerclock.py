# python script for the printerclock
# this script updates the segment on the clock every 30 mins until 11pm at night
# the script drives a stepper motor driver to set the position of the printer
# the file 'currentpos.txt' should be in the working directory and will be accessed every time the system starts. This way the printer can keep a record of it's current position.
import RPi.GPIO as GPIO
import time
import os

persistentfile = "currentpos.txt"
steps_per_segment = 272

segdict = {'early': '0',
    '1:00': '272',
    '1:30': '544',
    '2:00': '816',
    '2:30': '1088',
    '3:00': '1360',
    '3:30': '1632',
    '4:00': '1904',
    '4:30': '2176',
    '5:00': '2448',
    '5:30': '2720',
    '6:00': '2992',
    '6:30': '3264',
    '7:00': '3536',
    '7:30': '3808',
    '8:00': '4080',
    '8:30': '4352',
    '9:00': '4624',
    '9:30': '4896',
    '10:00': '5168',
    '10:30': '5440',
    '11:00': '5712',
    '11:30': '5984',
    '12:00': '6256',
    'late': '6528',
    'party': '6800'}

class stepperMotor:
    delay = 0.0008

    def __init__(self, clkpin, dirpin, enpin):
        self.clkpin = clkpin
        self.dirpin = dirpin
        self.enpin = enpin
        self.usedPins = [self.clkpin, self.dirpin, self.enpin]
        if os.path.exists(persistentfile):
            with open(persistentfile) as openfile:
                self.current_position = int(openfile.read())
                print "current position is:{}".format(self.current_position)
        else:
            self.current_position = 0
        print "configuring GPIO"
        GPIO.setmode(GPIO.BOARD)
        for pin in self.usedPins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(self.enpin, GPIO.LOW)

    def step(self, direction):
        if direction == 'CW':
            GPIO.output(self.dirpin, GPIO.LOW)
            self.current_position += 1
        elif direction == 'CCW':
            GPIO.output(self.dirpin, GPIO.HIGH)
            self.current_position -= 1
        else:
            return
        time.sleep(stepperMotor.delay)  # sleep 5us
        GPIO.output(self.clkpin, GPIO.HIGH)
        time.sleep(stepperMotor.delay)  # sleep 5us
        GPIO.output(self.clkpin, GPIO.LOW)

    def savepositiontofile(self):
        print self.current_position
        with open(persistentfile, mode='w') as of:
            of.write(str(self.current_position))

    def gotoposition(self, desired_position):
        # calculate offset
        movement = desired_position - self.current_position
        self.multistep(movement)

    def multistep(self, steps_to_do):
        if steps_to_do < 0:
            direction = 'CCW'
        else:
            direction = 'CW'
        steps = abs(steps_to_do)
        for single_step in range(steps):
            self.step(direction)
        self.savepositiontofile()

    def calibrate(self):
        self.current_position = 0




