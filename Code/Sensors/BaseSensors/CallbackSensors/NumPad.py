from Sensors.BaseSensors.BaseSensor import BaseSensor
from Actuators.BaseActuators.BuzzerStates.SingleBeep import SingleBeep
import RPi.GPIO as GPIO
import logging
from time import time, sleep

from Sensors.BaseSensors.CallbackSensors.CallbackSensor import CallbackSensor

logger = logging.getLogger(__name__)


class NumPad(CallbackSensor):

    ROW_DIMENSION = 4
    COLUMN_DIMENSION = 3
    STROKE_INTERVAL = 0.4
    BEEP_DURATION = 0.15

    def __init__(self, row_pins, column_pins, keys, buzzer, callback_function=None):
        super(NumPad, self).__init__(callback_function)
        self.__buzzer = buzzer
        self.__keys = keys
        self.__row_pins = row_pins
        self.__column_pins = column_pins
        self.__last_stroke = time()
        logging.debug("NumPad generated with row pins: {row_pins}, col pins: {col_pins}, callback function: {callback} "
                      "and keys: {keys}".format(row_pins=self.__row_pins,
                                                col_pins=self.__column_pins,
                                                callback=self.callback_function,
                                                keys=self.__keys))
        GPIO.setup(self.__column_pins, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.__row_pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.__current_col_check = 0

    def detect(self):
        GPIO.output(self.__column_pins[self.__current_col_check], GPIO.LOW)
        for row_pin in self.__row_pins:
            if GPIO.input(row_pin) == GPIO.LOW:
                row = self.__row_pins.index(row_pin)
                col = self.__current_col_check
                self.__key_pressed(row, col)
        GPIO.output(self.__column_pins[self.__current_col_check], GPIO.HIGH)
        self.__current_col_check = (self.__current_col_check + 1) % len(self.__column_pins)
        # yield processor
        sleep(0.000001)

    def __key_pressed(self, row, col):
        if self.__last_stroke + self.STROKE_INTERVAL > time():
            logger.debug("double stroke detected")
        else:
            logger.info("key {key} pressed with value {value}".format(key=self.__keys[row*3 + col],
                                                                      value=self.__keys[row*3 + col].get_value()))
            self.__last_stroke = time()
            self.__buzzer.set_state(SingleBeep(self.__buzzer,
                                               duration=self.BEEP_DURATION,
                                               returning_state=self.__buzzer.state))
            self.callback_function(self.__keys[row*3 + col])

    def destroy(self):
        self.__buzzer.stop()

    def run(self):
        while not self.exit_flag:
            self.detect()
        self.destroy()
