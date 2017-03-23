from LEDState import LEDState


class Red(LEDState):

    def __init__(self, led, duration=-1, returning_state=None):
        super(Red, self).__init__(led, duration, returning_state)
        self.actuator.red()

    def return_to(self):
        self.actuator.red()