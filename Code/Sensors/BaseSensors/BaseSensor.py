from Sensors.Sensor import Sensor
from abc import ABCMeta, abstractmethod


class BaseSensor(Sensor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_value(self):
        raise NotImplementedError()
