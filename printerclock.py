# python script for the printerclock
# this script updates the segment on the clock every 30 mins until 11pm at night
# the script drives a stepper motor driver to set the position of the printer
# the file 'currentpos.txt' should be in the working directory and will be accessed every time the system starts. This way the printer can keep a record of it's current position.
import RPi.GPIO as GPIO
import time
import os

persistentfile = "currentpos.txt"
steps_per_segment = 272
minposition = 0
maxposition = 6800

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
    '12:30': '6256',
    'late': '6528',
    'party': '6800'}


def gettime():
    hrs = time.localtime().tm_hour
    mins = time.localtime().tm_min
    dow = time.localtime().tm_wday
    return hrs, mins, dow

def getposition(hrs, mins, dow):
    if mins >= 30:
        mm = '30'
    else:
        mm = '00'

    wday = dow
    if (wday == 5 and hrs > 20) or (wday == 6 and hrs<7):
        search = 'party'

    elif hrs >= 23 or hrs < 7:
        search = 'late'
    else:
        if hrs>12:
            hrs-=12
        search='{}:{}'.format(hrs, mm)
    print hrs, mins, search
    return int(segdict[search])


class stepperMotorA4988:
    delay = 0.001

    def __init__(self, pindict):
        # pin dict should take a standard format for the A4988
        # pin_dict = {'clkpin':0,
        #             'dirpin':1,}
        self.pindict = pindict
        self.reqpins = ['dirpin',
                        'steppin',
                        'sleeppin',
                        'resetpin',
                        'ms3pin',
                        'ms2pin',
                        'ms1pin',
                        'enpin']
        self.override = False
        self.sleep = True
        if os.path.exists(persistentfile):
            with open(persistentfile) as openfile:
                self.current_position = int(openfile.read())
                print "current position is:{}".format(self.current_position)
        else:
            self.current_position = 0
        print "configuring GPIO"
        GPIO.setmode(GPIO.BCM)

        # set all pins as outputs
        for pinname in self.reqpins:
            print self.pindict[pinname]
            GPIO.setup(self.pindict[pinname], GPIO.OUT, initial=GPIO.LOW)

        # configure multistepping
        mspinnames = ['ms3pin', 'ms2pin', 'ms1pin']
        for pinname in mspinnames:
            GPIO.output(self.pindict[pinname], GPIO.LOW)

        time.sleep(0.001)  # 1ms delay
        #take driver out of sleep
        if self.pindict['sleeppin'] is not None:
            GPIO.output(self.pindict['sleeppin'], GPIO.HIGH)
            GPIO.output(self.pindict['resetpin'], GPIO.HIGH)
            time.sleep(0.002)  # 2ms delay

    def step(self, direction):
        if direction == 'CW':
            GPIO.output(self.pindict['dirpin'], GPIO.LOW)
            if self.current_position < maxposition or self.override:
                self.current_position += 1
            else:
                return
        elif direction == 'CCW':
            GPIO.output(self.pindict['dirpin'], GPIO.HIGH)
            if self.current_position > minposition or self.override:
                self.current_position -= 1
            else:
                return
        else:
            return
        time.sleep(stepperMotorA4988.delay)  # sleep 5us
        GPIO.output(self.pindict['steppin'], GPIO.HIGH)
        time.sleep(stepperMotorA4988.delay)  # sleep 5us
        GPIO.output(self.pindict['steppin'], GPIO.LOW)

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

        if steps != 0:
            # bring device out of sleep
            if self.pindict['sleeppin'] is not None:
                GPIO.output(self.pindict['sleeppin'], GPIO.HIGH)
                time.sleep(0.002)  # 2ms delay

            for single_step in range(steps):
                self.step(direction)
            self.savepositiontofile()

            # put device back into sleep
            if self.pindict['sleeppin'] is not None and self.sleep:
                GPIO.output(self.pindict['sleeppin'], GPIO.LOW)
                time.sleep(0.002)  # 2ms delay

    def calibrate(self):
        self.current_position = 0

    def override(self, newstate):
        self.override = newstate




