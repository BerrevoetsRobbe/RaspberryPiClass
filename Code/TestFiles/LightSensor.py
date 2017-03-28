import logging
import RPi.GPIO as GPIO

from time import sleep
from Actuators.BaseActuators.LED import LED
from Sensors.BaseSensors.PollingSensors.LightSensor import LightSensor


def test_general(light_sensor, led):
    while True:
        logging.info("light sensor value: {value}".format(value=light_sensor.get_value()))
        if light_sensor.get_value() == 0:
            led.perform_action_idle()
            sleep(0.000001)
        if light_sensor.get_value() == 1:
            led.perform_action_activated()
            sleep(0.000001)


def test_light_sensor(args):
    light_sensor = LightSensor(int(args[0]))
    led = LED(int(args[1]), int(args[2]))

    try:
        test_general(light_sensor, led)
    finally:
        light_sensor.destroy()
        led.destroy()
        sleep(1)
        GPIO.cleanup()
