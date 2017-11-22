import RPi.GPIO as GPIO
import stepmotor as sm
from nymph_pins.py import *

sm.StepperMotorTB6560(pin_dict_TB6560, sm.StepperMotorTB6560.type, 0, 6800)