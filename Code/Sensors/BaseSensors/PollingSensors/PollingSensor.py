from Sensors.BaseSensors.BaseSensor import BaseSensor
from abc import ABCMeta, abstractmethod


class PollingSensor(BaseSensor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_value(self):
        raise NotImplementedError()
