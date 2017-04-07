from Actuators.CustomActuators.MultipleLEDStates.AllBlank import AllBlank
from Actuators.CustomActuators.MultipleLEDStates.AllFlashRed import AllFlashRed
from Actuators.CustomActuators.MultipleLEDStates.AllGreen import AllGreen
from Actuators.CustomActuators.MultipleLEDStates.AllRed import AllRed
from CustomActuator import CustomActuator
import logging

logger = logging.getLogger(__name__)


class MultipleLED(CustomActuator):

    TRIGGER_PERIOD = 0.5

    def __init__(self, leds):
        super(MultipleLED, self).__init__(None)
        self.__leds = leds
        self.set_state(AllBlank(self))

    def perform_action_idle(self, duration=-1):
        logger.debug("MultipleLED performing idle action")
        self.set_state(AllGreen(self, duration=duration, returning_state=self.state))

    def perform_action_activated(self, duration=-1):
        logger.debug("MultipleLED performing activated action")
        self.set_state(AllRed(self, duration=duration, returning_state=self.state))

    def perform_action_triggered(self, duration=-1):
        logger.debug("MultipleLED performing triggered action")
        self.set_state(AllFlashRed(self, self.TRIGGER_PERIOD, duration=duration, returning_state=self.state))

    def destroy(self):
        logger.info("MultipleLED cleanup")
        for led in self.__leds:
            led.stop()

    def get_leds(self):
        return self.__leds
