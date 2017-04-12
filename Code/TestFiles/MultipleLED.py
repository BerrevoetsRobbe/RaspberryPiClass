#!/usr/bin/env python
#
# give combination of r_pin g_pin as arg
#
import RPi.GPIO as GPIO
import sys

from Actuators.BaseActuators.LED import LED
from Actuators.CustomActuators.MultipleLED import MultipleLED
from time import time, sleep
import logging


IDLE_TIME = 10
ACTIVATION_TIME = 10
TRIGGERED_TIME = 10


def test_general(multiple_led):
    multiple_led.perform_action_idle()
    start_time = time()
    while start_time + IDLE_TIME > time():
        # yield processor
        sleep(0.00001)
    start_time = time()
    multiple_led.perform_action_activated(ACTIVATION_TIME)
    while start_time + ACTIVATION_TIME + 3 > time():
        # yield processor
        sleep(0.00001)
    multiple_led.perform_action_triggered(TRIGGERED_TIME)


def test_multiple_led(args):
    if len(args) % 2 == 1:
        logging.info("there must be an equal amount of red and green pins")
        logging.warning("Het aantal pin nummers dat je meegeeft moet even zijn")
        sys.exit(1)
    logging.warning("Testen van meerdere LEDs")
    leds = [LED(int(args[i]), int(args[i+1])) for i in range(0, len(args), 2)]
    for led in leds:
        led.start()

    logging.debug("setting up multiple led with leds: {leds}".format(leds=leds))

    multiple_led = MultipleLED(leds)
    multiple_led.start()
    try:
        test_general(multiple_led)
        while True:
            # yield processor
            sleep(0.00001)
    finally:
        multiple_led.stop()
        multiple_led.join(2)
        sleep(4)
        GPIO.cleanup()
