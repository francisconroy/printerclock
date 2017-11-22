import threading
import time
import printerclock as pc
import BaseHTTPServer
import RPi.GPIO as GPIO
import httpserver
import doorstat as ds
import stepmotor as sm
import nymph_pins as np
import dooropener as do

## Configure threads
class ClockThread(threading.Thread):
    def run(self):
        clockstepper = sm.StepperMotorA4988(np.pin_dict_a4988, sm.StepperMotorA4988.type, 0, 6800)
        while 1:
            h, m, d = pc.gettime()
            pos = pc.getposition(h, m, d)
            clockstepper.gotoposition(pos)
            time.sleep(30)

class HTTPThread(threading.Thread):
    def run(self):
        ## Web server config
        server_address = ('', 80)
        import auth
        configfile = auth.ConfigFile("userdata.txt")
        configfile.print_users()

        door_status = ds.DoorStat(np.pin_dict_door_status)

        door_driver = sm.StepperMotorTB6560(np.pin_dict_TB6560, sm.StepperMotorTB6560.type, 0, 260)
        room_door = do.Door(door_status, door_driver)

        handler_class = httpserver.Server
        handler_class.getfunc = door_status.check_door_status
        handler_class.getfunc_args = ()
        handler_class.postfunc = configfile.checkpin_from_dict
        handler_class.postactionfunc = room_door.open_door
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class(server_address, handler_class)
        ## Init web server
        httpd.serve_forever()


## Start threads
print("Starting threads...")
clockthread = ClockThread(name="Clock thread")
clockthread.start()
httpthread = HTTPThread(name="HTTP thread")
httpthread.start()


