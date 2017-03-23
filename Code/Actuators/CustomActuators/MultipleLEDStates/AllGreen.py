from Actuators.BaseActuators.LEDState.Green import Green
from Actuators.CustomActuators.MultipleLEDStates.MultipleLEDState import MultipleLEDState


class AllGreen(MultipleLEDState):

    def __init__(self, multiple_led, duration=-1, returning_state=None):
        super(AllGreen, self).__init__(multiple_led, duration, returning_state)
        for led in self.actuator.get_leds():
            led.set_state(Green(led, duration=duration, returning_state=led.state))

    def return_to(self):
        for led in self.actuator.get_leds():
            led.set_state(Green(led, duration=self.duration, returning_state=led.state))
