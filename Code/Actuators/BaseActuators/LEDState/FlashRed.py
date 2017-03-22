from LEDState import LEDState
from time import time


class FlashRed(LEDState):

    def __init__(self, led, period, duration=-1, returning_state=None):
        super(FlashRed, self).__init__(led, duration, returning_state)
        self.period = period

    def perform_action(self):
        if (time()/self.period) % 2 >= 1:
            self.led.red()
        else:
            self.led.blank()
        super(FlashRed, self).perform_action()

    def return_to(self):
        pass
