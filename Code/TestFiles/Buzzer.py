#!/usr/bin/env python
# arg1 = buzzer_pin
import RPi.GPIO as GPIO
import logging

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
    buzzer = Buzzer(int(args[0]))
    buzzer.start()
    try:
        start_time = time()
        buzzer.perform_action_idle()
        while start_time + IDLE_TIME > time():
            # yield processor
            sleep(0.000001)
        buzzer.perform_action_activated()
        while start_time + IDLE_TIME + ACTIVATION_TIME > time():
            # yield processor
            sleep(0.000001)
        buzzer.perform_action_triggered(10)
        while True:
            # yield processor
            sleep(0.000001)
    finally:
        buzzer.stop()
        buzzer.join(2)
        GPIO.cleanup()
