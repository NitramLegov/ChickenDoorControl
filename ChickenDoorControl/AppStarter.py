import web

from routes.index import Index
import time

PossibleUrls = (
                '/favicon.ico', 'Favicon',
                '/(.*)', 'Index',
                '/', 'Index'
)

port_num = 8080

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
        web.httpserver.runsimple(Server.wsgifunc(), ("0.0.0.0", port_num))
    except Exception as e:
        print('An Error occurred:\n' + str(e))
        time.sleep(5)
    finally:
        cleanup()
