# arg1 = reed_pin, arg2 = r_pin, arg3 = g_pin
import logging
from time import sleep

import RPi.GPIO as GPIO
import sys

from Actuators.BaseActuators.Buzzer import Buzzer
from Sensors.BaseSensors.CallbackSensors.Keys.NumKey import NumKey
from Sensors.BaseSensors.CallbackSensors.Keys.SymbolKey import SymbolKey
from Sensors.CustomSensors.CallbackSensors.PinPad import PinPad


def create_key_list():
    logging.debug("start key creation")
    key_list = [NumKey(i) for i in range(1, 10)]
    key_list.append(SymbolKey('*'))
    key_list.append(NumKey(0))
    key_list.append(SymbolKey('#'))
    logging.debug("key list generated: {list}".format(list=key_list))
    return key_list


def test_pin_pad(args):
    if len(args) < 10:
        logging.info("You must give the row pins, column pins, the buzzer pin, the pin and an escape key")
        logging.warning("Je moet 4 'rij' pin nummers, 3 'kolom' pin nummers, de pin nummer van de buzzer, de pincode "
                        "en de resetknop (tussen ' ') meegeven. Dit zijn in totaal 10 waarden")
        sys.exit(1)
    logging.warning("Testen van het pinpad")
    row_pins = [int(arg) for arg in args[0:4]]
    col_pins = [int(arg) for arg in args[4:7]]
    buzzer_pin = int(args[7])
    pin = int(args[8])
    escape_key = args[9]
    buzzer = Buzzer(buzzer_pin)
    buzzer.start()
    keys = create_key_list()
    pin_pad = PinPad(row_pins, col_pins, keys, pin, escape_key, buzzer)
    logging.info("created numpad: {pinpad}".format(pinpad=pin_pad))
    try:
        while True:
            # yield processor
            sleep(0.000001)
    finally:
        logging.info('Cleanup pinpad')
        pin_pad.destroy()
        sleep(2)
        GPIO.cleanup()
