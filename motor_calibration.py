import stepmotor as sm
motors = [sm.StepperMotorTB6560(),
          sm.StepperMotorA4988()]




while(1):
    print("Motors:")
    for i in range(len(motors)):
        print(" {} - {}".format(i, motors[i].name))
    motor_index = raw_input("Please select a motor to calibrate:")
    print("Please use the a/d keys to position the motor")
    while(1):
        command = getch()
        if command == 'a':
            # Move CCW

        if command == 'd':
            # Move CW

        if command == ''

