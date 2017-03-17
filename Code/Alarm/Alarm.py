from AlarmState.Idle import Idle
from AlarmState.AlarmState import AlarmState
import logging

logger = logging.getLogger(__name__)


class Alarm(object):

    def __init__(self, actuators, activation_sensor, door_sensor):
        self.__alarm_state = Idle(self, actuators, AlarmState.DOOR_CLOSED)
        self.__activation_sensor = activation_sensor
        self.__door_sensor = door_sensor

    def loop(self):
        while True:
            # Activation
            if self.__activation_sensor.is_activated():
                self.__alarm_state.alarm_activated()
            else:
                self.__alarm_state.alarm_deactivated()
            # Door
            if self.__door_sensor.is_activated():
                self.__alarm_state.door_opened()
            else:
                self.__alarm_state.door_closed()

    def set_alarm_state(self, alarm_state):
        self.__alarm_state = alarm_state

    def get_alarm_state(self):
        return self.__alarm_state
