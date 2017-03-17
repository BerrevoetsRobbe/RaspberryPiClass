#!/usr/bin/env python
#
# give combination of r_pin g_pin as arg
#
import RPi.GPIO as GPIO

from Actuators.BaseActuators.LED import LED
from Actuators.CustomActuators.MultipleLED import MultipleLED
from time import time


IDLE_TIME = 10
ACTIVATION_TIME = 10
TRIGGERED_TIME = 10


def test_general(multiple_led):
    start_time = time()
    while start_time + IDLE_TIME > time():
        multiple_led.perform_action_idle()
    start_time = time()
    while start_time + ACTIVATION_TIME > time():
        multiple_led.perform_action_activated()
    start_time = time()
    while start_time + TRIGGERED_TIME > time():
        multiple_led.perform_action_triggered()


def test_multiple_led(args):
    if len(args) % 2 == 1:
        print "there must be an equal amount of red and green pins"

    leds = [LED(int(args[i]), int(args[i+1])) for i in range(0, len(args), 2)]
    multiple_led = MultipleLED(leds)
    try:
        test_general(multiple_led)
    finally:
        multiple_led.destroy()
        GPIO.cleanup()
