from CustomActuator import CustomActuator
import logging

logger = logging.getLogger(__name__)


class MultipleLED(CustomActuator):

    def __init__(self, leds):
        super(MultipleLED, self).__init__()
        self.__leds = leds

    def perform_action_idle(self):
        logger.debug("MultipleLED performing idle action")
        for led in self.__leds:
            led.perform_action_idle()

    def perform_action_activated(self):
        logger.debug("MultipleLED performing activated action")
        for led in self.__leds:
            led.perform_action_activated()

    def perform_action_triggered(self):
        logger.debug("MultipleLED performing triggered action")
        for led in self.__leds:
            led.perform_action_triggered()

    def destroy(self):
        logger.debug("MultipleLED cleanup")
        for led in self.__leds:
            led.destroy()
