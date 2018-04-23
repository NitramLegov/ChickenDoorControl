import time
import threading
import controller.door
import ephem
import datetime
try:
    import RPi.GPIO as GPIO
    running_on_pi = True
except:
    running_on_pi = False



class DoorAutomater(object):

    """description of class"""
    thread = None  # background thread that reads the distance from the sensor
    obs = ephem.Observer()
    obs.lat = '49.10318'
    obs.long = '8.47589'
    def initialize(self):
        if DoorAutomater.thread is None:
            # start background thread
            DoorAutomater.thread = threading.Thread(target=self._thread)
            DoorAutomater.thread.start()

    def start(self):
        self.initialize()
        return 'started'
    @classmethod
    def _thread(cls):
        obs = DoorAutomater.obs
        obs.date = datetime.datetime.utcnow()
        if obs.next_rising(ephem.Sun()) < obs.next_setting(ephem.Sun()):
            #it is night, close door
            print 'Initializing... It is night, so the door needs to be closed.'
            controller.door.down()
        else:
            #it is day, open door
            print 'Initializing... It is day, so the door needs to be open.'
            controller.door.up()
        while (True):
            obs.date = datetime.datetime.utcnow()
            #Testing line: 3 Seconds until Sunrise
            #obs.date = ephem.Date('2018/04/23 04:19:22.00')
            #Testing line: 3 Seconds until Sunset
            #obs.date = ephem.Date('2018/04/23 18:30:22.00')
            if obs.next_rising(ephem.Sun()) < obs.next_setting(ephem.Sun()):
                #it is night, next event is the sunrise
                next_event = 1
                time_to_sleep = (obs.next_rising(ephem.Sun()).datetime() - obs.date.datetime()).total_seconds()
            else:
                #it is day, next event is the sunset
                next_event = 0
                time_to_sleep = ((obs.next_setting(ephem.Sun()).datetime() - obs.date.datetime())).total_seconds()

            if next_event == 1:
                print "Currently it is nighttime. The door would go up at: " + str(ephem.localtime(obs.next_rising(ephem.Sun())))
                print "This means " + str(((obs.next_rising(ephem.Sun()).datetime() - obs.date.datetime())).total_seconds()) + " seconds"
                time.sleep(time_to_sleep)
                controller.door.up()
            else:
                print "Currently it is daytime. The door would go down at: " + str(ephem.localtime(obs.next_setting(ephem.Sun())))
                print "This means " + str(((obs.next_setting(ephem.Sun()).datetime() - obs.date.datetime())).total_seconds()) + " seconds"
                time.sleep(time_to_sleep)
                controller.door.down()
