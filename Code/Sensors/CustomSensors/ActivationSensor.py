from CustomSensor import CustomSensor
import logging

logger = logging.getLogger(__name__)


class ActivationSensor(CustomSensor):

    def __init__(self, sensor, active_value, deactive_value):
        super(ActivationSensor, self).__init__()
        self.__sensor = sensor
        self.__active_value = active_value
        self.__deactive_value = deactive_value

    def is_activated(self):
        return self.__sensor.get_value() == self.__active_value

    def is_deactivated(self):
        return self.__sensor.get_value() == self.__deactive_value
