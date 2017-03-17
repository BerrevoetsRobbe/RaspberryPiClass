#!/usr/bin/env python
# arg1 = reed_pin, arg2 = r_pin, arg3 = g_pin
import logging
import RPi.GPIO as GPIO

from Actuators.BaseActuators.LED import LED
from Sensors.BaseSensors.ReedSensor import ReedSensor


def test_reed_sensor(args):
    reed_sensor = ReedSensor(args[0])
    led = LED(args[1], args[2])

    try:
        while True:
            if reed_sensor.get_value() == 0:
                led.perform_action_idle()
            if reed_sensor.get_value() == 1:
                led.perform_action_activated()

    finally:
        logging.info("Cleanup LED and Reed Sensor")
        led.destroy()
        GPIO.cleanup()
