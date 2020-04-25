import stepmotor as sm
motors = [sm.StepperMotorTB6560(),
          sm.StepperMotorA4988()]

while 1:
    print("Motors:")
    for i in range(len(motors)):
        print(" {} - {}".format(i, motors[i].name))
    motor_index = input("Please select a motor to calibrate:")
    if motor_index >= len(motors):
        print("Invalid selection")
        exit(-1)
    motor = motors[motor_index]
    print("Move the motor to the zero position")
    while 1:
        command = input("cmd:")
        if command == 'c':
            print("saving cal")
            motor.calibrate()
        elif command == 'e':
            print("Exiting!")
            exit(0)
        else:
            try:
                value = int(command)
                motor.multistep(value)
            finally:
                pass


