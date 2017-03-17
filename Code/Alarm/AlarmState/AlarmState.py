from abc import ABCMeta, abstractmethod
import logging

logger = logging.getLogger(__name__)


class AlarmState(object):
    __metaclass__ = ABCMeta

    DOOR_CLOSED = -1
    DOOR_OPEN = 1

    def __init__(self, alarm, actuators, door_state):
        self.__alarm = alarm
        self.__actuators = actuators
        self.__door_state = door_state

    @abstractmethod
    def perform_action(self):
        raise NotImplementedError()

    @abstractmethod
    def alarm_activated(self):
        raise NotImplementedError()

    @abstractmethod
    def alarm_deactivated(self):
        raise NotImplementedError()

    @abstractmethod
    def door_opened(self):
        self.__door_state = self.DOOR_OPEN

    @abstractmethod
    def door_closed(self):
        self.__door_state = self.DOOR_CLOSED

    def get_actuators(self):
        return self.__actuators

    def get_alarm(self):
        return self.__alarm

    def set_alarm_state(self, alarm_state):
        self.__alarm.set_alarm_state(alarm_state)

    def is_door_open(self):
        return self.__door_state == self.DOOR_OPEN

    def get_door_state(self):
        return self.__door_state
