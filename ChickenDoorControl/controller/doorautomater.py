
import time
import threading
import controller.door

try:
    import RPi.GPIO as GPIO
    running_on_pi = True
except:
    running_on_pi = False



class DoorAutomater(object):

    """description of class"""
    thread = None  # background thread that reads the distance from the sensor
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if DoorAutomater.thread is None:
            # start background thread
            DoorAutomater.thread = threading.Thread(target=self._thread)
            DoorAutomater.thread.start()

    def getDistance(self):
        DistanceController.last_access = time.time()
        self.initialize()
        return self.currentDist
    @classmethod
    def _thread(cls):
        if running_on_pi:
            controller.door.up()
        else:
            cls.currentDist = "Not running on a pi or RPi.GPIO library not installed"
            cls.thread = None
