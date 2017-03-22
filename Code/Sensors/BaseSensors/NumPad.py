from BaseSensor import BaseSensor
import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class NumPad(BaseSensor):

    ROW_DIMENSION = 4
    COLUMN_DIMENSION = 3

    def __init__(self, input_row_pins, input_column_pins, keys, callback_function=None):
        self.__keys = keys
        self.__callback_function = callback_function or self.detect
        self.__input_row_pins = input_row_pins
        self.__input_column_pins = input_column_pins
        self.setup()

    def setup(self):
        # TODO: setup can accept a list
        for pin in self.__input_column_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.__callback_function, bouncetime=400)
        for pin in self.__input_row_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_value(self):
        return self.detect()

    def detect(self):
        row_val = -1
        col_val = -1
        for i in range(len(self.__input_row_pins)):
            tmp_read = GPIO.input(self.__input_row_pins[i])
            if tmp_read == 0:
                row_val = i
        for i in range(len(self.__input_column_pins)):
            tmp_read = GPIO.input(self.__input_column_pins[i])
            if tmp_read == 0:
                col_val = i

        if row_val == -1 or col_val == -1:
            return None
        else:
            logger.info("key pressed: {key}".format(key=self.__keys[col_val*row_val-1]))
            return self.__keys[col_val*row_val-1]
