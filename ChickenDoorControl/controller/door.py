import time
import threading
import ephem
import datetime


try:
    import RPi.GPIO as GPIO
    running_on_pi = True
except:
    running_on_pi = False

if running_on_pi:
    GPIO.setmode(GPIO.BCM)
    #We assume that turning the door up or down only needs the change of 1 pin:
    UP_PIN = 1
    DOWN_PIN = 2
    GPIO.setup(UP_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(DOWN_PIN, GPIO.OUT, initial=GPIO.LOW)
def up():
    if running_on_pi:
        GPIO.output(UP_PIN,GPIO.HIGH)
        time.sleep(10)
        GPIO.output(UP_PIN,GPIO.LOW)
    else:
        print 'not running on a pi. Door would have gone up at: ' + str(datetime.datetime.now())
def down():
    if running_on_pi:
        GPIO.output(DOWN_PIN,GPIO.HIGH)
        time.sleep(10)
        GPIO.output(DOWN_PIN,GPIO.LOW)
    else:
        print 'not running on a pi. Door would have gone down at: ' + str(datetime.datetime.now())