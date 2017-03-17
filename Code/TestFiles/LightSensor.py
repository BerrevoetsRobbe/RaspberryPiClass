#!/usr/bin/env python
# arg1 = light_pin, arg2 = r_pin, arg3 = g_pin
import logging
import RPi.GPIO as GPIO

from Actuators.BaseActuators.LED import LED
from Sensors.BaseSensors.LightSensor import LightSensor


IDLE_TIME = 10
ACTIVATION_TIME = 10
TRIGGERED_TIME = 10


def test_general(light_sensor, led):
    while True:
        logging.info("light sensor value: {value}".format(value=light_sensor.get_value()))
        if light_sensor.get_value() == 0:
            led.perform_action_idle()
        if light_sensor.get_value() == 1:
            led.perform_action_activated()


def test_light_sensor(args):
    light_sensor = LightSensor(int(args[0]))
    led = LED(int(args[1]), int(args[2]))

    try:
        test_general(light_sensor, led)
    finally:
        logging.info("Cleanup LED and lightsensor")
        led.destroy()
        GPIO.cleanup()
