from AlarmState import AlarmState


class Activated(AlarmState):

    def perform_action(self):
        pass

    def __init__(self, alarm, actuators, door_state):
        super(Activated, self).__init__(alarm, actuators, door_state)
        for actuator in self.__actuators:
            actuator.perform_action_activated()

    def door_opened(self):
        super(Activated, self).door_opened()
        from Triggered import Triggered
        self.set_alarm_state(Triggered(self.get_alarm(), self.get_actuators(), self.get_door_state()))

    def door_closed(self):
        super(Activated, self).door_closed()

    def alarm_deactivated(self):
        from Idle import Idle
        self.set_alarm_state(Idle(self.get_alarm(), self.get_actuators(), self.get_door_state()))

    def alarm_activated(self):
        pass
