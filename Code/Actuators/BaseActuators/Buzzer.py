from BaseActuator import BaseActuator
from time import time
import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class Buzzer(BaseActuator):

    BUZZER_SOUND_OUTPUT = GPIO.LOW
    BUZZER_MUTE_OUTPUT = GPIO.HIGH

    def __init__(self, buzzer_pin):
        super(Buzzer, self).__init__()
        self.__buzzer_pin = buzzer_pin
        self.__mute_buzzer()

    def perform_action_idle(self):
        logger.debug("Buzzer performing idle action")
        self.__mute_buzzer()

    def perform_action_activated(self):
        logger.debug("Buzzer performing activated action")
        self.__mute_buzzer()

    def perform_action_triggered(self):
        logger.debug("Buzzer performing triggered action")
        if time() % 2 >= 1:
            self.__sound_buzzer()
        else:
            self.__mute_buzzer()

    def __sound_buzzer(self):
        GPIO.setup(self.__buzzer_pin, GPIO.OUT)
        GPIO.output(self.__buzzer_pin, self.BUZZER_SOUND_OUTPUT)

    def __mute_buzzer(self):
        GPIO.setup(self.__buzzer_pin, GPIO.OUT)
        GPIO.output(self.__buzzer_pin, self.BUZZER_MUTE_OUTPUT)
        GPIO.setup(self.__buzzer_pin, GPIO.IN)

    def destroy(self):
        logger.debug("Buzzer cleanup")
        GPIO.output(self.__buzzer_pin, self.BUZZER_MUTE_OUTPUT)