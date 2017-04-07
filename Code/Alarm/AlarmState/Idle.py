import logging

from AlarmState import AlarmState


class Idle(AlarmState):

    def __init__(self, alarm, door_state, duration=-1, return_state=None):
        super(Idle, self).__init__(alarm, door_state, duration, return_state)
        for actuator in self.get_actuators():
            actuator.perform_action_idle()

    def door_opened(self):
        super(Idle, self).door_opened()

    def door_closed(self):
        super(Idle, self).door_closed()

    def alarm_deactivated(self):
        pass

    def alarm_activated(self):
        from Activated import Activated
        from Triggered import Triggered
        if self.is_door_open():
            self.set_alarm_state(Triggered(self.get_alarm(),
                                           self.get_door_state(),
                                           duration=Triggered.TRIGGER_DURATION,
                                           return_state=Activated))
        else:
            self.set_alarm_state(Activated(self.get_alarm(), self.get_door_state()))

    def refresh(self):
        for actuator in self.get_actuators():
            actuator.perform_action_idle()
