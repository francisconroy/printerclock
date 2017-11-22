# the file 'currentpos.txt' should be in the working directory and will be accessed
# every time the system starts. This way the printer can keep a record of it's current position.
import RPi.GPIO as GPIO
import time
import os


## Generic stepper motor driver class
# @ brief Generic class for each driver type
class StepperMotor:
    persistentfile_template = "currentpos_{}.txt"
    delay = 0.001
    # init is generic
    def __init__(self, pindict, name, minposition, maxposition, override=False):
        self.name = name
        self.maxposition = maxposition
        self.minposision = minposition
        self.pindict = pindict
        self.persistentfile = StepperMotor.persistentfile_template.format(name)

        self.override = override
        self.sleep = True

        ## Init position
        if os.path.exists(self.persistentfile):
            with open(self.persistentfile) as openfile:
                self.current_position = int(openfile.read())
                print("current position is:{}".format(self.current_position))
        else:
            self.current_position = 0
        print("configuring GPIO")
        self.pin_init()

    # user to implement
    def pin_init(self):
        pass

    # User to implement
    # @brief Function which allows the driver to make a single step in the given direction
    # @param direction direction as a string either 'CW' or 'CCW'
    # In general this function must be implemented for each motor driver instance
    def step(self, direction):
        pass

    # user to implement
    def sleepmode(self, state):
        pass

    # class generic
    def savepositiontofile(self):
        print(self.current_position)
        with open(self.persistentfile, mode='w') as of:
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
            self.sleepmode(False) # Take the driver out of sleep
            for single_step in range(steps):
                self.step(direction)
            self.sleepmode(True) # put the driver back to sleep
            self.savepositiontofile()

    def calibrate(self):
        self.current_position = 0

    def override(self, newstate):
        self.override = newstate

class StepperMotorA4988(StepperMotor):
    delay = 0.001
    type = "A4988"

    def pin_init(self):
        self.reqpins = ['dirpin',
                        'steppin',
                        'sleeppin',
                        'resetpin',
                        'ms3pin',
                        'ms2pin',
                        'ms1pin',
                        'enpin']

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
        self.sleepmode(False)

    def step(self, direction):
        self.sleepmode(False)
        if direction == 'CW':
            GPIO.output(self.pindict['dirpin'], GPIO.HIGH)
            if self.current_position < self.maxposition or self.override:
                self.current_position += 1
            else:
                return
        elif direction == 'CCW':
            GPIO.output(self.pindict['dirpin'], GPIO.LOW)
            if self.current_position > self.minposition or self.override:
                self.current_position -= 1
            else:
                return
        else:
            return
        time.sleep(StepperMotorA4988.delay)  # sleep 5us
        GPIO.output(self.pindict['steppin'], GPIO.HIGH)
        time.sleep(StepperMotorA4988.delay)  # sleep 5us
        GPIO.output(self.pindict['steppin'], GPIO.LOW)

    def sleepmode(self, state):
        if state:
            GPIO.output(self.pindict['sleeppin'], GPIO.LOW)
            time.sleep(0.002)  # 2ms delay
        else:
            GPIO.output(self.pindict['sleeppin'], GPIO.HIGH)
            time.sleep(0.002)  # 2ms delay


class StepperMotorTB6560(StepperMotor):
    delay = 0.001
    type = "TB6560"

    def pin_init(self):
        pass
        self.reqpins = ['clkpin',  # does one step on the driver when you enable it
                        'dirpin',  # change direction of stepping (CW or CCW)
                        'sleeppin']  # takes driver out of sleep
        # set all pins as outputs
        for pinname in self.reqpins:
            print(self.pindict[pinname])
            GPIO.setup(self.pindict[pinname], GPIO.OUT, initial=GPIO.LOW)
        time.sleep(0.001)  # 1ms delay

        # take driver out of sleep
        if self.pindict['sleeppin'] is not None:
            GPIO.output(self.pindict['sleeppin'], GPIO.LOW)
            GPIO.output(self.pindict['clkpin'], GPIO.HIGH)
            time.sleep(0.002)  # 2ms delay

    def step(self, direction):
        self.sleepmode(False)
        if direction == 'CW':
            GPIO.output(self.pindict['dirpin'], GPIO.HIGH)
            if self.current_position < self.maxposition or self.override:
                self.current_position += 1
            else:
                return
        elif direction == 'CCW':
            GPIO.output(self.pindict['dirpin'], GPIO.LOW)
            if self.current_position > self.minposition or self.override:
                self.current_position -= 1
            else:
                return
        else:
            return
        time.sleep(StepperMotor.delay)  # sleep 5us
        GPIO.output(self.pindict['clkpin'], GPIO.HIGH)
        time.sleep(StepperMotor.delay)  # sleep 5us
        GPIO.output(self.pindict['clkpin'], GPIO.LOW)