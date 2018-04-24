import time
import threading
import controller.door
import ephem
import datetime
from controller.doorautomater import DoorAutomater
try:
    import RPi.GPIO as GPIO
    running_on_pi = True
except:
    running_on_pi = False

class WatchDog(object):

    """description of class"""
    thread = None  # background thread
    status = None
    def initialize(self):
        if WatchDog.thread is None:
            # start background thread
            WatchDog.thread = threading.Thread(target=self._thread)
            WatchDog.thread.start()
            # wait until the watchdog got initialized
            while self.status is None:
                time.sleep(0)

    def start(self):
        self.initialize()
        return WatchDog.status


    @classmethod
    def _thread(cls):
        while (True):
            WatchDog.status = DoorAutomater.thread.is_alive()
            #print str(WatchDog.status)
            if WatchDog.status and running_on_pi:
                with open('/dev/watchdog', 'wb') as watchdog_file:
                    watchdog_file.write('1')
            time.sleep(5)
