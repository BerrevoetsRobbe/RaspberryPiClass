from BaseSensor import BaseSensor
from NumPad import NumPad
import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class PinPad(BaseSensor):

    def __init__(self, input_row_pins, input_column_pins, keys, pin, escape_key):
        self.__numpad = NumPad(input_row_pins, input_column_pins, keys, self.register_key)
        self.__pin = pin
        self.__escape_key = escape_key
        self.__key_history = []
        self.__activated = -1

    def get_value(self):
        return self.__activated

    def register_key(self):
        key = self.__numpad.get_value() # object Key
        if key is None:
            return
        if key == self.__escape_key:
            logger.debug("escape key entered")
            self.__key_history = []
        else:
            logger.debug("key {key} entered".format(key=key.get_value()))
            self.__key_history.append(key.get_value())

        self.__check_key_history()

    def __check_key_history(self):
        if self.__key_history == self.__pin:
            self.__pin_entered()
            self.__key_history = []

    def __pin_entered(self):
        logger.info("pin entered")
        self.__activated *= -1
