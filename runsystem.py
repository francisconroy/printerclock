import threading
import time
import printerclock as pc
import BaseHTTPServer
import RPi.GPIO as GPIO
import httpserver
import doorstat as ds


## General config
pin_dict = {'dirpin': 4,  # a4988 breakout PCB
            'steppin': 17,
            'sleeppin': 27,
            'resetpin': 22,
            'ms3pin': 18,
            'ms2pin': 25,
            'ms1pin': 24,
            'enpin': 23,
            'doorpin': 12}  # door status

GPIO.setmode(GPIO.BCM)

## Configure threads
class ClockThread(threading.Thread):
    def run(self):
        clockstepper = pc.stepperMotorA4988(pin_dict)
        while 1:
            h, m, d = pc.gettime()
            pos = pc.getposition(h, m, d)
            clockstepper.gotoposition(pos)
            time.sleep(30)

## Web server config
server_address = ('', 80)

print("Initialising the system...")
ds.do_init(pin_dict)
handler_class = httpserver.S
handler_class.getfunc = ds.check_door_status(pin_dict)
server_class = BaseHTTPServer.HTTPServer
httpd = server_class(server_address, handler_class)

## Start threads
print("Starting threads...")
clockthread = ClockThread(name="Clock thread")
clockthread.start()

## Init web server
httpd.serve_forever()