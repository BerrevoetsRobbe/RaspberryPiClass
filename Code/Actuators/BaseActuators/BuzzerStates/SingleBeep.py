from Actuators.BaseActuators.BuzzerStates.BuzzerState import BuzzerState


class Mute(BuzzerState):
    def __init__(self, buzzer, duration=-1, returning_state=None):
        super(Mute, self).__init__(buzzer, duration, returning_state)
        self.actuator.sound_buzzer()

    def return_to(self):
        self.actuator.sound_buzzer()
