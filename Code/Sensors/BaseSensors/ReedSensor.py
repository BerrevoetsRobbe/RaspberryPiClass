from BaseSensor import BaseSensor
import RPi.GPIO as GPIO


class ReedSensor(BaseSensor):

    def __init__(self, input_pin):
        self.__input_pin = input_pin
        GPIO.setup(self.__input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set BtnPin's mode is input, and pull up to high level(3.3V)

    def get_value(self):
        return GPIO.input(self.__input_pin)

    def destroy(self):
        pass