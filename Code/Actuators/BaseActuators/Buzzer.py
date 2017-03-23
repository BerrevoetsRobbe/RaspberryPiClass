from Actuators.BaseActuators.BuzzerStates.Mute import Mute
from Actuators.BaseActuators.BuzzerStates.MultipleBeeps import MultipleBeeps
from BaseActuator import BaseActuator
from time import time
import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class Buzzer(BaseActuator):

    BUZZER_SOUND_OUTPUT = GPIO.LOW
    BUZZER_MUTE_OUTPUT = GPIO.HIGH
    TRIGGER_PERIOD = .5

    def __init__(self, buzzer_pin):
        super(Buzzer, self).__init__(None)
        self.__buzzer_pin = buzzer_pin
        self.set_state(Mute(self))

    def perform_action_idle(self, duration=-1):
        logger.debug("Buzzer performing idle action")
        self.set_state(Mute(self, duration=duration,returning_state=self.state))

    def perform_action_activated(self, duration=-1):
        logger.debug("Buzzer performing activated action")
        self.set_state(Mute(self, duration=duration, returning_state=self.state))

    def perform_action_triggered(self, duration=-1):
        logger.debug("Buzzer performing triggered action")
        self.set_state(MultipleBeeps(self, self.TRIGGER_PERIOD, duration=duration, returning_state=self.state))

    def sound_buzzer(self):
        logging.debug("start sounding buzzer {buzzer}".format(buzzer=self))
        GPIO.setup(self.__buzzer_pin, GPIO.OUT)
        GPIO.output(self.__buzzer_pin, self.BUZZER_SOUND_OUTPUT)

    def mute_buzzer(self):
        logging.debug("mute buzzer {buzzer}".format(buzzer=self))
        GPIO.setup(self.__buzzer_pin, GPIO.OUT)
        GPIO.output(self.__buzzer_pin, self.BUZZER_MUTE_OUTPUT)
        GPIO.setup(self.__buzzer_pin, GPIO.IN)

    def destroy(self):
        logger.debug("Buzzer cleanup")
        GPIO.setup(self.__buzzer_pin, GPIO.OUT)
        GPIO.output(self.__buzzer_pin, self.BUZZER_MUTE_OUTPUT)