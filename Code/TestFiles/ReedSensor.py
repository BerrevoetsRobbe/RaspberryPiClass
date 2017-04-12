import RPi.GPIO as GPIO

from time import sleep

import logging

import sys

from Actuators.BaseActuators.LED import LED
from Sensors.BaseSensors.PollingSensors.ReedSensor import ReedSensor


def test_reed_sensor(args):
    if len(args) < 3:
        logging.info("You must give the reed sensor pin and the two pins of the LED")
        logging.warning("Je moet 1 pin nummer van de magneet sensor geven en de 2 pin nummers van de LED sensor")
        sys.exit(1)
    logging.warning("Testen van de magneet sensor")
    reed_sensor = ReedSensor(int(args[0]))
    led = LED(int(args[1]), int(args[2]))
    last_value = -1
    try:

        while True:
            if reed_sensor.get_value() == 0 and reed_sensor.get_value() != last_value:
                logging.warning("De magneet sensor neemt een magneet waar")
                last_value = 0
                led.perform_action_activated()
                sleep(0.000001)
            if reed_sensor.get_value() == 1 and reed_sensor.get_value() != last_value:
                logging.warning("De magneet sensor neemt een magneet waar")
                last_value = 1
                led.perform_action_idle()
                sleep(0.000001)

    finally:
        led.stop()
        reed_sensor.destroy()
        sleep(0.5)
        GPIO.cleanup()
