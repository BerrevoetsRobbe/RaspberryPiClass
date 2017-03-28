from threading import Thread
from time import sleep

from Sensors.CustomSensors.CustomSensor import CustomSensor


class ThresholdSensor(CustomSensor, Thread):

    def __init__(self, base_sensor, threshold, callback_below, callback_above):
        super(ThresholdSensor, self).__init__()
        self.__base_sensor = base_sensor
        self.__threshold = threshold
        self.__callback_below = callback_below
        self.__callback_above = callback_above
        self.__below = self.__base_sensor.get_value() < self.__threshold
        self.__exit_flag = False

    def run(self):
        while not self.__exit_flag:
            if self.__below and self.__base_sensor.get_value() >= self.__threshold:
                self.__below = False
                self.__callback_above()
            elif not self.__below and self.__base_sensor.get_value() < self.__threshold:
                self.__below = True
                self.__callback_below()
            sleep(0.000001)  # yield processor

        self.destroy()

    def stop(self):
        self.__exit_flag = True

    def destroy(self):
        pass
