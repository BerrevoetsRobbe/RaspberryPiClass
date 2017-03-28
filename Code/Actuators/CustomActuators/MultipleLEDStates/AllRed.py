from Actuators.BaseActuators.LEDStates.Red import Red
from Actuators.CustomActuators.MultipleLEDStates.MultipleLEDState import MultipleLEDState


class AllRed(MultipleLEDState):

    def __init__(self, multiple_led, duration=-1, returning_state=None):
        super(AllRed, self).__init__(multiple_led, duration, returning_state)
        for led in self.actuator.get_leds():
            led.set_state(Red(led, duration=duration, returning_state=led.state))

    def return_to(self):
        for led in self.actuator.get_leds():
            led.set_state(Red(led, duration=self.duration, returning_state=led.state))
