import printerclock as pc

# a4988 breakout PCB
pin_dict = {'dirpin': 4,
            'steppin': 17,
            'sleeppin': 27,
            'resetpin': 22,
            'ms3pin': 18,
            'ms2pin': 25,
            'ms1pin': 24,
            'enpin': 23}

clockstepper = pc.stepperMotorA4988(pin_dict)
clockstepper.multistep(100)


