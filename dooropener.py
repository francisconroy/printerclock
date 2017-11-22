import stepmotor as sm
import RPi.GPIO as GPIO
import doorstat as ds
import stepmotor as sm


class Door(object):
    def __init__(self, door_status, driver):
        #
        self.door_status = door_status
        self.door_driver = driver

    def open_door(self):
        start_position = self.door_driver.current_position
        print("Not open")
        while(not self.door_status.check_door_status()):
            #self.door_driver.step('CW') # add steps
            print("Not open")
        print("Door is opened")
        # Return driver to initial position
        #self.door_driver.gotoposition(start_position)


def main():
    import nymph_pins as np
    door_status = ds.DoorStat(np.pin_dict_door_status)
    door_driver = sm.StepperMotorTB6560(np.pin_dict_TB6560, sm.StepperMotorTB6560.type, 0, 260)
    room_door = Door(door_status, door_driver)
    room_door.open_door()
    print("Door is open!")

if __name__ == "__main__":
    main()
