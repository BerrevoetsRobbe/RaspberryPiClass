import logging
import RPi.GPIO as GPIO

from time import time
from Sensors.BaseSensors.BaseSensor import BaseSensor


class ReedSensor(BaseSensor):

    CACHE_FRESHNESS_INTERVAL = 0.1

    def __init__(self, input_pin):
        self.__input_pin = input_pin
        GPIO.setup(self.__input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.__cache_time = time()
        self.__cached_value = GPIO.input(self.__input_pin)

    def get_value(self):
        if self.__cache_time + self.CACHE_FRESHNESS_INTERVAL < time():
            self.__cache_time = time()
            self.__cached_value = GPIO.input(self.__input_pin)
        return self.__cached_value

    def destroy(self):
        logging.debug("Cleanup ReedSensor")
        pass
