from threading import Thread
from time import sleep

from Sensors.CustomSensors.CustomSensor import CustomSensor


class ValuesSensor(CustomSensor, Thread):

    def __init__(self, sensor, values, callback_functions):
        super(ValuesSensor, self).__init__()
        self.__sensor = sensor
        self.__values = values
        self.__callback_functions = callback_functions
        self.__exit_flag = False
        self.__last_value = self.__sensor.get_value()

    def run(self):
        while not self.__exit_flag:
            current_value = self.__sensor.get_value()
            if self.__last_value != current_value and current_value in self.__values:
                self.__last_value = current_value
                self.__callback_functions[self.__values.index(current_value)]()

            sleep(0.000001)
        self.destroy()

    def stop(self):
        self.__exit_flag = True

    def destroy(self):
        pass