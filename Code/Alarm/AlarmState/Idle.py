from AlarmState import AlarmState


class Idle(AlarmState):

    def __init__(self, alarm, actuators, door_state):
        super(Idle, self).__init__(alarm, actuators, door_state)
        for actuator in self.get_actuators():
            actuator.perform_action_idle()

    def door_opened(self):
        super(Idle, self).door_opened()

    def door_closed(self):
        super(Idle, self).door_closed()

    def perform_action(self):
        pass

    def alarm_deactivated(self):
        pass

    def alarm_activated(self):
        if self.is_door_open():
            from Triggered import Triggered
            self.set_alarm_state(Triggered(self.get_alarm(), self.get_actuators(), self.get_door_state()))
        else:
            from Activated import Activated
            self.set_alarm_state(Activated(self.get_alarm(), self.get_actuators(), self.get_door_state()))