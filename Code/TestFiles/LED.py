#!/usr/bin/env python
# arg1 = r_pin, arg2 = g_pin
import sys
import RPi.GPIO as GPIO
import logging

from Actuators.BaseActuators.LED import LED
from time import time

IDLE_TIME = 10
ACTIVATION_TIME = 10
TRIGGERED_TIME = 20


def test_general(_led):
    start_time = time()
    while start_time + IDLE_TIME > time():
        _led.perform_action_idle()
    start_time = time()
    while start_time + ACTIVATION_TIME > time():
        _led.perform_action_activated()
    start_time = time()
    while start_time + TRIGGERED_TIME > time():
        _led.perform_action_triggered()


def test_triggered(_led):
    start_time = time()
    while start_time + TRIGGERED_TIME > time():
        _led.perform_action_triggered()


def test_led(args):
    if len(args) < 2:
        print("You must give r and g pin as arguments")
        sys.exit(1)
    led = LED(int(args[0]), int(args[1]))
    try:
        test_triggered(led)
    finally:
        logging.info("Cleanup LED")
        led.destroy()
        GPIO.cleanup()
