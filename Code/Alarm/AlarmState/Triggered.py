import time

import logging

from AlarmState import AlarmState


class Triggered(AlarmState):

    TRIGGER_DURATION = 5

    def __init__(self, alarm, door_state, duration=-1, return_state=None):
        super(Triggered, self).__init__(alarm, door_state, duration, return_state)
        for actuator in self.get_actuators():
            actuator.perform_action_triggered()

    def door_opened(self):
        super(Triggered, self).door_opened()

    def door_closed(self):
        super(Triggered, self).door_closed()

    def alarm_deactivated(self):
        from Idle import Idle
        self.set_alarm_state(Idle(self.get_alarm(), self.get_door_state()))

    def alarm_activated(self):
        pass

    def refresh(self):
        for actuator in self.get_actuators():
            actuator.perform_action_triggered()
