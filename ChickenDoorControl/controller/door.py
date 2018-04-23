import time
import threading
import ephem
import datetime
import controller.settings as settings

try:
    import RPi.GPIO as GPIO
    running_on_pi = True
except:
    running_on_pi = False

if running_on_pi:
    GPIO.setmode(GPIO.BCM)
    #We assume that turning the door up or down only needs the change of 1 pin:
    UP_PIN = settings.configuration.getint('Doorcontrol','UP_PIN')
    DOWN_PIN = settings.configuration.getint('Doorcontrol','UP_PIN')
    time_needed = settings.configuration.getint('Doorcontrol','TIME')
    GPIO.setup(UP_PIN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(DOWN_PIN, GPIO.OUT, initial=GPIO.HIGH)
def up():
    if running_on_pi:
        GPIO.output(UP_PIN,GPIO.LOW)
        time.sleep(time_needed)
        GPIO.output(UP_PIN,GPIO.HIGH)
    else:
        print 'not running on a pi. Door would have gone up at: ' + str(datetime.datetime.now())
def down():
    if running_on_pi:
        GPIO.output(DOWN_PIN,GPIO.LOW)
        time.sleep(time_needed)
        GPIO.output(DOWN_PIN,GPIO.HIGH)
    else:
        print 'not running on a pi. Door would have gone down at: ' + str(datetime.datetime.now())