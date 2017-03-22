import logging

from abc import ABCMeta, abstractmethod
from time import time


class LEDState(object):
    __metaclass__ = ABCMeta

    def __init__(self, led, duration=-1, returning_state=None):
        logging.debug("initialising LED state with led {led}, duration {duration}s"
                      " and returning state: {state}".format(led=led,
                                                             duration=duration,
                                                             state=returning_state))
        self.led = led
        self.duration = duration
        self.returning_state = returning_state
        self.start_time = time()

    def perform_action(self):
        if self.duration != -1 and self.start_time + self.duration < time() and self.returning_state:
            logging.debug("Return to previous state {state}".format(state=self.returning_state))
            self.led.set_state(self.returning_state)
            self.returning_state.return_to()

    @abstractmethod
    def return_to(self):
        raise NotImplementedError()
