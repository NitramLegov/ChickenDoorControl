import web

from routes.index import Index
from routes.settings import Settings
import time
from controller.doorautomater import DoorAutomater
from controller.watchdog import WatchDog
import controller.settings as settings
import sys

PossibleUrls = (
                '/favicon.ico', 'Favicon',
                '/api/settings', 'Settings',
                '/api/settings/(.*)/(.*)', 'Settings',
                '/api/settings/(.*)', 'Settings',
                '/(.*)', 'Index',
                '/', 'Index'
)

port_num = settings.configuration.getint('Server','port')

def cleanup():
    print ('cleaning up before exit..')
    
    try:
        import RPi.GPIO as GPIO
        GPIO.cleanup()
    except:
        print('nothing')

if __name__ == "__main__":
    Server = web.application(PossibleUrls,globals())

    try:
        WatchDog().start() 
        #print DoorAutomater().get_next_event()
        web.httpserver.runsimple(Server.wsgifunc(), ("0.0.0.0", port_num))
    except Exception as e:
        print('An Error occurred:\n' + str(e))
        time.sleep(5)
    finally:
        cleanup()
