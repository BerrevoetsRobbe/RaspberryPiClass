from LEDState import LEDState


class Blank(LEDState):

    def return_to(self):
        self.led.blank()

    def __init__(self, led, duration=-1, returning_state=None):
        super(Blank, self).__init__(led, duration, returning_state)
        self.led.blank()
