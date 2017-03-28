from Actuators.BaseActuators.LEDStates.FlashRed import FlashRed
from Actuators.CustomActuators.MultipleLEDStates.MultipleLEDState import MultipleLEDState


class AllFlashRed(MultipleLEDState):

    def __init__(self, multiple_led, period, duration=-1, returning_state=None):
        super(AllFlashRed, self).__init__(multiple_led, duration, returning_state)
        self.period = period
        for led in self.actuator.get_leds():
            led.set_state(FlashRed(led, self.period, duration=duration, returning_state=led.state))

    def return_to(self):
        for led in self.actuator.get_leds():
            led.set_state(FlashRed(led, self.period, duration=self.duration, returning_state=led.state))
