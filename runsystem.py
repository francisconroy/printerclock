import threading
import time
import printerclock as pc
import BaseHTTPServer
import RPi.GPIO as GPIO
import httpserver
import doorstat as ds
import stepmotor as sm


## General config
GPIO.setmode(GPIO.BCM)

# A4988 pins
pin_dict_a4988 = {'dirpin': 4,
            'steppin': 17,
            'sleeppin': 27,
            'resetpin': 22,
            'ms3pin': 18,
            'ms2pin': 25,
            'ms1pin': 24,
            'enpin': 23}
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

## Configure threads
class ClockThread(threading.Thread):
    def run(self):
        clockstepper = sm.StepperMotorA4988(pin_dict_a4988, "A4988", 0, 6800)
        while 1:
            h, m, d = pc.gettime()
            pos = pc.getposition(h, m, d)
            clockstepper.gotoposition(pos)
            time.sleep(30)

## Web server config
server_address = ('', 80)

print("Initialising the system...")
ds.do_init(pin_dict_door_status)
handler_class = httpserver.S
handler_class.getfunc = ds.check_door_status(pin_dict_door_status)
server_class = BaseHTTPServer.HTTPServer
httpd = server_class(server_address, handler_class)

## Start threads
print("Starting threads...")
clockthread = ClockThread(name="Clock thread")
clockthread.start()

## Init web server
httpd.serve_forever()