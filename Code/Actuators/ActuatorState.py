import logging

from abc import ABCMeta, abstractmethod
from time import time, sleep


class ActuatorState(object):
    __metaclass__ = ABCMeta

    def __init__(self, actuator, duration=-1, returning_state=None):
        logging.debug("initialising actuator state with device {actuator}, duration {duration}s"
                      " and returning state: {state}".format(actuator=actuator,
                                                             duration=duration,
                                                             state=returning_state))
        self.actuator = actuator
        self.duration = duration
        self.returning_state = returning_state
        self.start_time = time()

    def perform_action(self):
        if not(self.duration != -1 and self.start_time + self.duration < time() and self.returning_state):
            # yield processor
            sleep(0.000001)
        else:
            logging.debug("Return to previous state {state}".format(state=self.returning_state))
            self.actuator.set_state(self.returning_state)
            self.returning_state.return_to()

    @abstractmethod
    def return_to(self):
        raise NotImplementedError()
