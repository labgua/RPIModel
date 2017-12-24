# coding=utf-8

import tornado.ioloop
import tornado.web

from RPIModel.RPIWebSocket import RPIWebSocket

import os

import signal
import sys



try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

GPIO.setmode(GPIO.BOARD)

## necessario se più di uno script sta usando le GPIO
GPIO.setwarnings(False)



print("WEBSOCKET RPI!!")

def signal_handler(signal, frame):
        GPIO.cleanup()
        print('GPIO.cleanup DONE!')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



path = os.getcwd();





app = tornado.web.Application([
    ('/ws', RPIWebSocket),
    ('/(.*\..*)', tornado.web.StaticFileHandler, {'path': path + "/static"})
])

if __name__ == "__main__":
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()