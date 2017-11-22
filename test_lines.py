import RPi.GPIO as GPIO
import stepmotor as sm
import nymph_pins as np

doormotor = sm.StepperMotorTB6560(np.pin_dict_TB6560, sm.StepperMotorTB6560.type, 0, 6800)