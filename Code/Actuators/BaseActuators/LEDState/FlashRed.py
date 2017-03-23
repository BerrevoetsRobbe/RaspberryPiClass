from LEDState import LEDState
from time import time, sleep


class FlashRed(LEDState):

    def __init__(self, led, period, duration=-1, returning_state=None):
        super(FlashRed, self).__init__(led, duration, returning_state)
        self.period = period
        self.actuator.blank()
        self.color_shown = False

    def perform_action(self):
        show_color = (time() / self.period) % 2 - 1 >= 0
        if show_color and not self.color_shown:
            self.color_shown = True
            self.actuator.red()
        elif not show_color and self.color_shown:
            self.color_shown = False
            self.actuator.blank()
        else:
            # yield processor
            sleep(0.000001)
        super(FlashRed, self).perform_action()

    def return_to(self):
        pass
