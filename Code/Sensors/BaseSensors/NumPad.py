from BaseSensor import BaseSensor
from Actuators.BaseActuators.BuzzerStates.SingleBeep import SingleBeep
import RPi.GPIO as GPIO
import logging
import time

logger = logging.getLogger(__name__)


class NumPad(BaseSensor):

    ROW_DIMENSION = 4
    COLUMN_DIMENSION = 3
    BOUNCE_TIME = 500
    STROKE_INTERVAL = 0.3
    BEEP_DURATION = 0.15

    def __init__(self, input_row_pins, input_column_pins, keys, buzzer, callback_function=None):
        self.__buzzer = buzzer
        self.__keys = keys
        self.__callback_function = callback_function or self.detect
        self.__input_row_pins = input_row_pins
        self.__input_column_pins = input_column_pins
        self.__last_stroke = time.time()
        logging.debug("NumPad generated with row pins: {row_pins}, col pins: {col_pins}, callback function: {callback} "
                      "and keys: {keys}".format(row_pins=self.__input_row_pins,
                                                col_pins=self.__input_column_pins,
                                                callback=self.__callback_function,
                                                keys=self.__keys))
        GPIO.setup(self.__input_column_pins, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.__input_row_pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for pin in self.__input_row_pins:
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.__callback_function, bouncetime=self.BOUNCE_TIME)
            # self.setup()

    def setup(self):
        # TODO: setup can accept a list
        for pin in self.__input_column_pins:
            GPIO.setup(self.__input_column_pins, GPIO.OUT, initial=GPIO.LOW)
            GPIO.output(pin, GPIO.LOW)
        for pin in self.__input_row_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.__callback_function, bouncetime=self.BOUNCE_TIME)

    def get_value(self):
        return self.detect_raw()

    def detect(self, channel):

        row_val = self.__input_row_pins.index(channel)

        logging.debug("key on row {row} pressed".format(row=row_val))

        self.set_row_pin_to_output(channel)
        self.set_column_pins_to_input()

        col_val = -1

        for pin in self.__input_column_pins:
            tmp_read = GPIO.input(pin)
            if tmp_read == 1:
                col_val = self.__input_column_pins.index(pin)

        logging.debug("key on column {col} pressed".format(col=col_val))

        self.set_row_pin_to_input(channel)

        if self.__last_stroke + self.STROKE_INTERVAL > time.time():
            logger.debug("double stroke detected")
            return None
        elif row_val == -1 or col_val == -1:
            return None
        else:
            logger.info("key {key} pressed with value {value}".format(key=self.__keys[row_val*3 + col_val],
                                                                      value=self.__keys[row_val*3 + col_val].get_value()))
            self.__last_stroke = time.time()
            self.__buzzer.set_state(SingleBeep(self.__buzzer, duration=self.BEEP_DURATION, returning_state=self.__buzzer.state))
            return self.__keys[row_val*3 + col_val]

    def set_column_pins_to_input(self):
        for pin in self.__input_column_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def set_column_pins_to_output(self):
        GPIO.setup(self.__input_column_pins, GPIO.OUT, initial=GPIO.LOW)

    def set_row_pin_to_input(self, pin_number):
        GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin_number, GPIO.FALLING, callback=self.__callback_function, bouncetime=self.BOUNCE_TIME)

    def set_row_pin_to_output(self, pin_number):
        GPIO.remove_event_detect(pin_number)
        GPIO.setup(pin_number, GPIO.OUT)
        GPIO.output(pin_number, GPIO.HIGH)

    def detect_raw(self):

        row_pin = -1
        for pin in self.__input_row_pins:
            tmpRead = GPIO.input(pin)
            if tmpRead == 0:
                row_pin = pin

        if row_pin == -1:
            return None

        self.set_row_pin_to_output(row_pin)
        self.set_column_pins_to_input()

        col_pin = -1
        for pin in self.__input_column_pins:
            tmpRead = GPIO.input(pin)
            if tmpRead == 1:
                col_pin = pin

        self.set_row_pin_to_input(row_pin)
        self.set_column_pins_to_output()

        if col_pin == -1:
            return None
        else:
            row_number = self.__input_row_pins.index(row_pin)
            col_number = self.__input_column_pins.index(col_pin)
            logger.info("key {key} pressed with value {value}".format(key=self.__keys[row_number*3 + col_number],
                                                                      value=self.__keys[row_number*3 + col_number].get_value()))
            return self.__keys[row_number*3 + col_number]

    def destroy(self):
        self.__buzzer.stop()
