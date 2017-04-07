from abc import ABCMeta, abstractmethod
import logging
from time import time, sleep

logger = logging.getLogger(__name__)


class AlarmState(object):
    __metaclass__ = ABCMeta

    DOOR_CLOSED = -1
    DOOR_OPEN = 1

    def __init__(self, alarm, door_state, duration=-1, return_state=None):
        self.__alarm = alarm
        self.__door_state = door_state
        self.duration = duration
        self.return_state = return_state
        self.start_time = time()

    def time_check(self):
        if not(self.duration != -1 and self.start_time + self.duration < time() and self.return_state):
            # yield processor
            sleep(0.000001)
            logging.debug("time check with start time {start_time}, duration {duration}, time {time} "
                          "and return state {return_state}".format(start_time=self.start_time,
                                                                   duration=self.duration,
                                                                   time=time(),
                                                                   return_state=self.return_state))
        else:
            self.__alarm.set_alarm_state(self.return_state(self.get_alarm(), self.get_door_state()))
            self.__alarm.refresh()
            logging.debug("Return to previous state {state}".format(state=self.__alarm.get_alarm_state()))

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

    @abstractmethod
    def refresh(self):
        raise NotImplementedError()

    def get_actuators(self):
        return self.get_alarm().get_actuators()

    def get_alarm(self):
        return self.__alarm

    def set_alarm_state(self, alarm_state):
        self.__alarm.set_alarm_state(alarm_state)

    def is_door_open(self):
        return self.__door_state == self.DOOR_OPEN

    def get_door_state(self):
        return self.__door_state
