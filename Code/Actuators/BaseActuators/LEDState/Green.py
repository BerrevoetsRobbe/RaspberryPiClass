from LEDState import LEDState


class Green(LEDState):

    def __init__(self, led, duration=-1, returning_state=None):
        super(Green, self).__init__(led, duration, returning_state)
        self.actuator.green()

    def return_to(self):
        self.actuator.green()

