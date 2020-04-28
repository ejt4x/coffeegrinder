#!/usr/bin/env python3

import subprocess, shlex
from RPi import GPIO
from time import sleep
import threading
import logging
import argparse

SHUTDOWN_CMD = 'sudo shutdown -h now'
REBOOT_CMD = 'sudo reboot'

RELAY_PIN=17
DEFAULT_GRIND_TIME=5 #seconds
MAX_GRIND_TIME=30.0

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper
   

class CoffeeGrinder(object):

    def __init__(self):
        self.isGrinding=False
        logging.basicConfig(level=logging.INFO)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_PIN, GPIO.OUT)

    def cleanup(self):
        while self.isGrinding:
            sleep(0.1)
        GPIO.cleanup()

    def halt(self):
        logging.warning("Halting")
        self.cleanup()
        args = shlex.split(SHUTDOWN_CMD)
        subprocess.call(args)
        return 0

    def reboot(self):
        logging.warning("Rebooting")
        self.cleanup()
        args = shlex.split(REBOOT_CMD)
        subprocess.call(args)
        return 0

    def start_grind(self):
        logging.info("Starting grind")
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        self.isGrinding=True
        return True

    def stop_grind(self):
        logging.info("Stopping grind")
        GPIO.output(RELAY_PIN, GPIO.LOW)
        self.isGrinding=False
        return True
        
    #@threaded
    def timed_grind(self, seconds, callback=lambda: None):
        if seconds > MAX_GRIND_TIME: seconds = MAX_GRIND_TIME

        logging.info("Grinding for {} seconds".format(seconds))
        self.start_grind()
        sleep(seconds)
        self.stop_grind()

        callback()

        logging.info("Grinding complete")
        return 0

def main():
    grinder = CoffeeGrinder()

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', \
            default=DEFAULT_GRIND_TIME, \
            type=int )
    args = parser.parse_args()
    logging.debug(args)

    grinder.timed_grind(args.duration)
    sleep(1)
    grinder.cleanup()

if __name__ == "__main__":
    main()
