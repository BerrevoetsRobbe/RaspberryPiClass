# arg1 = reed_pin, arg2 = r_pin, arg3 = g_pin
import logging
from time import sleep

import RPi.GPIO as GPIO
from Sensors.BaseSensors.NumKey import NumKey
from Sensors.BaseSensors.SymbolKey import SymbolKey

from Actuators.BaseActuators.Buzzer import Buzzer
from Sensors.BaseSensors.CallbackSensors.NumPad import NumPad


def create_key_list():
    logging.debug("start key creation")
    key_list = [NumKey(i) for i in range(1, 10)]
    key_list.append(SymbolKey('*'))
    key_list.append(NumKey(0))
    key_list.append(SymbolKey('#'))
    logging.debug("key list generated: {list}".format(list=key_list))
    return key_list


def test_num_pad(args):
    row_pins = [int(arg) for arg in args[0:4]]
    col_pins = [int(arg) for arg in args[4:7]]
    buzzer_pin = int(args[7])
    buzzer = Buzzer(buzzer_pin)
    buzzer.start()
    keys = create_key_list()
    numpad = NumPad(row_pins, col_pins, keys, buzzer)
    numpad.start()
    logging.info("created numpad: {numpad}".format(numpad=numpad))
    try:
        while True:
            # yield processor
            sleep(0.000001)
    finally:
        logging.info('Cleanup numpad')
        numpad.stop()
        sleep(2)
        GPIO.cleanup()
