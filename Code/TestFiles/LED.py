#!/usr/bin/env python
# arg1 = r_pin, arg2 = g_pin
import sys
import RPi.GPIO as GPIO
import logging

from Actuators.BaseActuators.LED import LED
from time import sleep

IDLE_TIME = 10
ACTIVATION_TIME = 10
TRIGGERED_TIME = 10


def test_general(_led):
    # unable to use time() to often
    _led.perform_action_idle(duration=IDLE_TIME)
    _led.perform_action_activated(duration=ACTIVATION_TIME)
    _led.perform_action_triggered(duration=TRIGGERED_TIME)


def test_triggered(_led):
    _led.perform_action_triggered(duration=TRIGGERED_TIME)


def test_led(args):
    if len(args) < 2:
        print("You must give r and g pin as arguments")
        sys.exit(1)
    led = LED(int(args[0]), int(args[1]))
    led.start()
    try:
        led.perform_action_idle()
        led.perform_action_triggered(duration=TRIGGERED_TIME)
        while True:
            # yield processor
            sleep(0.000001)
    finally:
        led.stop()
        led.join(2)
        GPIO.cleanup()
