# arg1 = reed_pin, arg2 = r_pin, arg3 = g_pin
import logging
import RPi.GPIO as GPIO

from Sensors.BaseSensors.NumPad import NumPad
from Sensors.BaseSensors.NumKey import NumKey
from Sensors.BaseSensors.SymbolKey import SymbolKey


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
    keys = create_key_list()
    num_pad = NumPad(row_pins, col_pins, keys)
    logging.info("created numpad: {numpad}".format(numpad=num_pad))
    try:
        while True:
            pass

    finally:
        logging.info('Cleanup numpad')
        GPIO.cleanup()
