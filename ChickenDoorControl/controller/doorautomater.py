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
    thread = None  # background thread
    next_event = None
    time_of_next_event = None
    obs = ephem.Observer()
    obs.lat = '49.10318'
    obs.long = '8.47589'
    def initialize(self):
        if DoorAutomater.thread is None:
            # start background thread
            DoorAutomater.thread = threading.Thread(target=self._thread)
            DoorAutomater.thread.daemon = True
            DoorAutomater.thread.start()
            # wait until the next event got calculated
            while self.next_event is None or self.time_of_next_event is None:
                time.sleep(0)

    def get_next_event(self):
        self.initialize()
        return 'Next Event: ' + DoorAutomater.next_event + ' at: ' + str(DoorAutomater.time_of_next_event)


    @classmethod
    def _thread(cls):
        obs = DoorAutomater.obs
        obs.date = datetime.datetime.utcnow()
        if obs.next_rising(ephem.Sun()) < obs.next_setting(ephem.Sun()):
            #it is night, close door
            DoorAutomater.next_event = 'Sunrise'
            DoorAutomater.time_of_next_event = ephem.localtime(obs.next_rising(ephem.Sun()))
            print 'Initializing... It is night, so the door needs to be closed.'
            controller.door.down()
        else:
            #it is day, open door
            DoorAutomater.next_event = 'Sunset'
            DoorAutomater.time_of_next_event = ephem.localtime(obs.next_setting(ephem.Sun()))
            print 'Initializing... It is day, so the door needs to be open.'
            controller.door.up()
        while (True):
            obs.date = datetime.datetime.utcnow()
            #Testing line: 3 Seconds until Sunrise
            #obs.date = ephem.Date('2018/04/23 04:19:22.00')
            #Testing line: 10 Seconds until Sunset
            #obs.date = ephem.Date('2018/04/23 18:30:15.00')
            if obs.next_rising(ephem.Sun()) < obs.next_setting(ephem.Sun()):
                #it is night, next event is the sunrise
                DoorAutomater.next_event = 'Sunrise'
                DoorAutomater.time_of_next_event = ephem.localtime(obs.next_rising(ephem.Sun()))
                time_to_sleep = (obs.next_rising(ephem.Sun()).datetime() - obs.date.datetime()).total_seconds()
            else:
                #it is day, next event is the sunset
                DoorAutomater.next_event = 'Sunset'
                DoorAutomater.time_of_next_event = ephem.localtime(obs.next_setting(ephem.Sun()))
                time_to_sleep = ((obs.next_setting(ephem.Sun()).datetime() - obs.date.datetime())).total_seconds()

            if DoorAutomater.next_event  == 'Sunrise':
                print "Currently it is nighttime. The door would go up at: " + str(ephem.localtime(obs.next_rising(ephem.Sun())))
                print "This means in " + str(((obs.next_rising(ephem.Sun()).datetime() - obs.date.datetime())).total_seconds()) + " seconds"
                time.sleep(time_to_sleep)
                controller.door.up()
            else:
                print "Currently it is daytime. The door would go down at: " + str(ephem.localtime(obs.next_setting(ephem.Sun())))
                print "This means in " + str(((obs.next_setting(ephem.Sun()).datetime() - obs.date.datetime())).total_seconds()) + " seconds"
                time.sleep(time_to_sleep)
                controller.door.down()
