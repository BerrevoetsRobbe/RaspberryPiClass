from Sensors.BaseSensors.BaseSensor import BaseSensor
import PCF8591 as ADC
import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)


class LightSensor(BaseSensor):

    def __init__(self, input_pin):
        self.__input_pin = input_pin
        ADC.setup(0x48)
        GPIO.setup(self.__input_pin, GPIO.IN)
        logger.info("LightSensor {light_sensor} initialized: ".format(light_sensor=self))

    def get_value(self):
        return ADC.read(0)

    def destroy(self):
        pass
