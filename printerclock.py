# python script for the printerclock
# this script updates the segment on the clock every 30 mins until 11pm at night
# the script drives a stepper motor driver to set the position of the printer
# the file 'currentpos.txt' should be in the working directory and will be accessed every time the system starts. This way the printer can keep a record of it's current position.
import RPi.GPIO as GPIO
import time
import calendar
import os

steps_per_segment = 272

segdict = {'early': '0',
    '1:00': '272',
    '1:30': '544',
    '2:00': '816',
    '2:30': '1088',
    '3:00': '1360',
    '3:30': '1632',
    '4:00': '1904',
    '4:30': '2176',
    '5:00': '2448',
    '5:30': '2720',
    '6:00': '2992',
    '6:30': '3264',
    '7:00': '3536',
    '7:30': '3808',
    '8:00': '4080',
    '8:30': '4352',
    '9:00': '4624',
    '9:30': '4896',
    '10:00': '5168',
    '10:30': '5440',
    '11:00': '5712',
    '11:30': '5984',
    '12:00': '6256',
    '12:30': '6256',
    'late': '6528',
    'party': '6800'}


def gettime():
    hrs = time.localtime().tm_hour
    mins = time.localtime().tm_min
    dow = time.localtime().tm_wday
    return hrs, mins, dow


def getposition(hrs, mins, dow):
    if mins >= 30:
        mm = '30'
    else:
        mm = '00'

    wday = dow
    if (wday in [calendar.FRIDAY, calendar.SATURDAY] and hrs > 18) \
            or (wday in [calendar.SATURDAY, calendar.SUNDAY] and hrs < 7):  # second part ensures that the clock doesn't jump to late at midnight
        search = 'party'
    elif hrs >= 22 or hrs < 7:
        search = 'late'
    else:
        if hrs > 12:
            hrs -= 12
        search = '{}:{}'.format(hrs, mm)
    print(hrs, mins, search)
    return int(segdict[search])
