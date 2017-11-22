import stepmotor as sm
import RPi.GPIO as GPIO
import doorstat as ds
import stepmotor as sm


class Door(object):
    def __init__(self, pin_dict_status, pin_dict_driver):
        self.pin_dict_status = pin_dict_status
        self.pin_dict_driver = pin_dict_driver

        #
        self.door_status = ds.DoorStat(self.pin_dict_status)
        self.door_driver = sm.StepperMotorTB6560("door_driver",0,260)

    def open_door(self):
        start_position = self.door_driver.current_position()
        print("Not open")
        while(not self.door_status):
            #self.door_driver.step('CW') # add steps
            print("Not open")
        print("Door is opened")
        # Return driver to initial position
        #self.door_driver.gotoposition(start_position)


def main():
    import nymph_pins as np

    room_door = Door(np.pin_dict_door_status, np.pin_dict_TB6560)
    room_door.open_door()
    print("Door is open!")

if __name__ == "__main__":
    main()
