import stepmotor as sm
import RPi.GPIO as GPIO
import doorstat as ds
import stepmotor as sm


sm.StepperMotorTB6560("door_motor", 0, 1000)


class Door(object):
    def __init__(self, pin_dict_status, pin_dict_driver):
        self.pin_dict_status = pin_dict_status
        self.pin_dict_driver = pin_dict_driver

        #
        self.door_status = ds.DoorStat(self.pin_dict_status)
        self.door_driver = sm.StepperMotorTB6560("door_driver",0,1000)

    def open_door(self):
        start_position = self.door_driver.current_position()
        while(not self.door_status):
            self.door_driver.step('CW')
        print("Door is opened")
        # Return driver to initial position
        self.door_driver.gotoposition(start_position)


def main():
    ## General config
    GPIO.setmode(GPIO.BCM)
    # TB6560 pins
    pin_dict_TB6560 = {'dirpin': 4,
                       'steppin': 17,
                       'sleeppin': 27,
                       'resetpin': 22,
                       'ms3pin': 18,
                       'ms2pin': 25,
                       'ms1pin': 24,
                       'enpin': 23}
    # door status pins
    pin_dict_door_status = {'doorpin': 12}

    room_door = Door(pin_dict_door_status, pin_dict_TB6560)
    room_door.open_door()
    print("Door is open!")


    # Calibration procedure for the door
    # Turn override ON
    # Move open the door, i.e. unwind the spool until the handle is fully up
    # perform calibrate to save the position to file
    # Actuate the door handle slowly until the door is open (checking the direction CW/CCW)
    # Confirm that the door status is known to be open
    # Set max as current position plus a small amount (safety allowance)
    # Turn override OFF
    # Run live test by calling open door

if __name__ == "__main__":
    main()
