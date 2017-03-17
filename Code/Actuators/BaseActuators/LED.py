from BaseActuator import BaseActuator
from time import time
import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class LED(BaseActuator):

    PWM_MIN_VALUE = 0
    PWM_MAX_VALUE = 100
    COLOR_MIN_VALUE = 0
    COLOR_MAX_VALUE = 255

    def __init__(self, r_pin, g_pin):
        super(LED, self).__init__()
        self.__r_pin = r_pin
        self.__g_pin = g_pin
        GPIO.setup([self.__r_pin, self.__g_pin], GPIO.OUT)  # Set pins' mode is output
        GPIO.output([self.__r_pin, self.__g_pin], GPIO.LOW)  # Set pins to LOW(0V) to off led

        self.__r_pulse = GPIO.PWM(self.__r_pin, 2000)  # set Frequece to 2KHz
        self.__g_pulse = GPIO.PWM(self.__g_pin, 2000)
        self.__r_pulse.start(0)  # Initial duty Cycle = 0(leds off)
        self.__g_pulse.start(0)

    def perform_action_idle(self):
        logger.debug("LED performing idle action")
        self.__green()

    def perform_action_activated(self):
        logger.debug("LED performing activated action")
        self.__red()

    def perform_action_triggered(self):
        logger.debug("LED performing triggered action")
        self.__flash_red()

    def __green(self):
        self.__r_pulse.ChangeDutyCycle(self.PWM_MIN_VALUE)     # Change duty cycle
        self.__g_pulse.ChangeDutyCycle(self.PWM_MAX_VALUE)

    def __red(self):
        self.__r_pulse.ChangeDutyCycle(self.PWM_MAX_VALUE)     # Change duty cycle
        self.__g_pulse.ChangeDutyCycle(self.PWM_MIN_VALUE)

    def __custom_color(self, r_value, g_value):
        self.__r_pulse(self.__map(r_value))
        self.__g_pulse(self.__map(g_value))

    def __map(self, x):
        return (x - self.COLOR_MIN_VALUE) / (self.COLOR_MAX_VALUE - self.COLOR_MIN_VALUE) \
               * (self.PWM_MAX_VALUE - self.PWM_MIN_VALUE) + self.PWM_MIN_VALUE

    def __turn_off(self):
        self.__r_pulse.stop()
        self.__g_pulse.stop()

    def __blank(self):
        self.__r_pulse.ChangeDutyCycle(self.PWM_MIN_VALUE)
        self.__g_pulse.ChangeDutyCycle(self.PWM_MIN_VALUE)

    def __flash_red(self):
        if time() % 2 >= 1:
            self.__red()
        else:
            self.__blank()

    def destroy(self):
        logger.debug("LED cleanup")
        self.__turn_off()
        GPIO.output([self.__r_pin, self.__g_pin], GPIO.LOW)

