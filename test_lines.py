
# Motors
import RPi.GPIO as GPIO
import stepmotor as sm
import nymph_pins as np

doormotor = sm.StepperMotorTB6560(np.pin_dict_TB6560, sm.StepperMotorTB6560.type, 0, 260)

clockmotor = sm.StepperMotorA4988(np.pin_dict_a4988, sm.StepperMotorA4988.type, 0, 6800)