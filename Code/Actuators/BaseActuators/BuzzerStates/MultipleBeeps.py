from time import time, sleep

from Actuators.BaseActuators.BuzzerStates.BuzzerState import BuzzerState


class MultipleBeeps(BuzzerState):

    def __init__(self, buzzer, period, duration=-1, returning_state=None):
        super(MultipleBeeps, self).__init__(buzzer, duration, returning_state)
        self.period = period
        self.actuator.mute_buzzer()
        self.beeping = False

    def perform_action(self):
        beep = (time() / self.period) % 2 - 1 >= 0
        if beep and not self.beeping:
            self.beeping = True
            self.actuator.sound_buzzer()
        elif not beep and self.beeping:
            self.beeping = False
            self.actuator.mute_buzzer()
        else:
            # yield processor
            sleep(0.000001)
        super(MultipleBeeps, self).perform_action()

    def return_to(self):
        pass
