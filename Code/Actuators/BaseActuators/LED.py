from BaseActuator import BaseActuator
from LEDStates.Blank import Blank
from LEDStates.Green import Green
from LEDStates.Red import Red
from LEDStates.FlashRed import FlashRed

import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class LED(BaseActuator):

    PWM_MIN_VALUE = 0
    PWM_MAX_VALUE = 100
    COLOR_MIN_VALUE = 0
    COLOR_MAX_VALUE = 255
    TRIGGER_PERIOD = .5

    def __init__(self, r_pin, g_pin):
        super(LED, self).__init__(None)
        self.__r_pin = r_pin
        self.__g_pin = g_pin
        GPIO.setup([self.__r_pin, self.__g_pin], GPIO.OUT)  # Set pins' mode is output
        GPIO.output([self.__r_pin, self.__g_pin], GPIO.LOW)  # Set pins to LOW(0V) to off led
        self.__r_pulse = GPIO.PWM(self.__r_pin, 2000)  # set Frequency to 2KHz
        self.__g_pulse = GPIO.PWM(self.__g_pin, 2000)
        self.__r_pulse.start(self.PWM_MIN_VALUE)  # Initial duty Cycle = 0(leds off)
        self.__g_pulse.start(self.PWM_MIN_VALUE)
        self.set_state(Blank(self))

    def perform_action_idle(self, duration=-1):
        logger.debug("LED performing idle action")
        self.set_state(Green(self, duration=duration, returning_state=self.state))

    def perform_action_activated(self, duration=-1):
        logger.debug("LED performing activated action")
        self.set_state(Red(self, duration=duration, returning_state=self.state))

    def perform_action_triggered(self, duration=-1):
        logger.debug("LED performing triggered action")
        self.set_state(FlashRed(self, self.TRIGGER_PERIOD, duration=duration, returning_state=self.state))

    def __map(self, x):
        return (x - self.COLOR_MIN_VALUE) / (self.COLOR_MAX_VALUE - self.COLOR_MIN_VALUE) \
               * (self.PWM_MAX_VALUE - self.PWM_MIN_VALUE) + self.PWM_MIN_VALUE

    def __turn_off(self):
        self.__r_pulse.stop()
        self.__g_pulse.stop()

    def __set_r_pulse(self, value):
        self.__r_pulse.ChangeDutyCycle(value)

    def __set_g_pulse(self, value):
        self.__g_pulse.ChangeDutyCycle(value)

    def green(self):
        self.__set_r_pulse(LED.PWM_MIN_VALUE)
        self.__set_g_pulse(LED.PWM_MAX_VALUE)

    def red(self):
        self.__set_r_pulse(LED.PWM_MAX_VALUE)
        self.__set_g_pulse(LED.PWM_MIN_VALUE)

    def blank(self):
        self.__set_r_pulse(LED.PWM_MIN_VALUE)
        self.__set_g_pulse(LED.PWM_MIN_VALUE)

    def custom_color(self, r_value, g_value):
        self.__set_r_pulse(self.__map(r_value))
        self.__set_r_pulse(self.__map(g_value))

    def destroy(self):
        logger.debug("LED cleanup")
        self.__turn_off()
        GPIO.output([self.__r_pin, self.__g_pin], GPIO.LOW)
