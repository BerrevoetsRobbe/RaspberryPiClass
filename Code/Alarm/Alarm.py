import logging

from threading import Thread
from AlarmState.Idle import Idle
from AlarmState.AlarmState import AlarmState

logger = logging.getLogger(__name__)


class Alarm(Thread):

    def __init__(self):
        super(Alarm, self).__init__()
        self.__actuators = []
        self.__alarm_state = Idle(self, AlarmState.DOOR_CLOSED)
        self.exit_flag = False

    def run(self):
        while not self.exit_flag:
            self.__alarm_state.time_check()
        self.destroy()

    def callback_activation(self, activated):
        if activated:
            self.__alarm_state.alarm_activated()
        else:
            self.__alarm_state.alarm_deactivated()

    def callback_door(self, opened):
        if opened:
            self.__alarm_state.door_opened()
        else:
            self.__alarm_state.door_closed()

    def set_alarm_state(self, alarm_state):
        logging.info("{alarm} switched to state {state}".format(alarm=self,
                                                                state=self.__alarm_state))
        self.__alarm_state = alarm_state

    def get_alarm_state(self):
        return self.__alarm_state

    def get_actuators(self):
        return self.__actuators

    def add_actuator(self, actuator):
        self.__actuators.append(actuator)

    def refresh(self):
        self.__alarm_state.refresh()

    def stop(self):
        self.exit_flag = True

    def destroy(self):
        for actuator in self.get_actuators():
            actuator.stop()
