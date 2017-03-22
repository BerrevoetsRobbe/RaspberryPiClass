import time

from AlarmState import AlarmState


class Triggered(AlarmState):

    TRIGGER_DURATION = 30

    def __init__(self, alarm, actuators, door_state):
        super(Triggered, self).__init__(alarm, actuators, door_state)
        self.__trigger_time = time.time()
        for actuator in self.get_actuators():
            actuator.perform_action_triggered()

    def door_opened(self):
        super(Triggered, self).door_opened()

    def door_closed(self):
        super(Triggered, self).door_closed()

    def perform_action(self):
        pass

    def alarm_deactivated(self):
        from Idle import Idle
        self.set_alarm_state(Idle(self.get_alarm(), self.get_actuators(), self.get_door_state()))

    def alarm_activated(self):
        pass

    def get_trigger_time(self):
        return self.__trigger_time