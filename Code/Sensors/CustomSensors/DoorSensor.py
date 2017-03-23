from CustomSensor import CustomSensor
import logging

logger = logging.getLogger(__name__)


class DoorSensor(CustomSensor):

    def __init__(self, sensor, open_value, closed_value):
        super(DoorSensor, self).__init__()
        self.__sensor = sensor
        self.__open_value = open_value
        self.__closed_value = closed_value

    def is_activated(self):
        return self.__sensor.get_value() == self.__open_value

    def is_deactivated(self):
        return self.__sensor.get_value() == self.__closed_value

    def destroy(self):
        pass
