from abc import ABCMeta, abstractmethod
from Sensors.CustomSensors.CustomSensor import CustomSensor


class PollingSensor(CustomSensor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_value(self):
        raise NotImplementedError()
