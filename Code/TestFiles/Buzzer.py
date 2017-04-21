#!/usr/bin/env python
# arg1 = buzzer_pin
import RPi.GPIO as GPIO
import logging

import sys

from Actuators.BaseActuators.Buzzer import Buzzer
from time import time, sleep

IDLE_TIME = 5
ACTIVATION_TIME = 5
TRIGGERED_TIME = 5


def test_idle(buzzer):
    pass


def test_activated(buzzer):
    pass


def test_triggered(buzzer):
    pass

def test_general(buzzer):
    test_idle(buzzer)
    test_activated(buzzer)
    test_triggered(buzzer)


def test_buzzer(args):
    if len(args) < 1:
        logging.info("You must give buzzer pin as arguments")
        logging.warning("Je moet minstens 1 pin nummer meegeven")
        sys.exit(1)
    buzzer = Buzzer(int(args[0]))
    buzzer.start()
    logging.warning("Testen van buzzer")
    try:
        buzzer.perform_action_triggered(10)
        while True:
            # yield processor
            sleep(0.000001)
    finally:
        buzzer.stop()
        buzzer.join(2)
        GPIO.cleanup()
