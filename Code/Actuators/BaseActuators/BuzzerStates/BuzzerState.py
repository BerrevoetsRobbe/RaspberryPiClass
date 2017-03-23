from abc import ABCMeta
from Actuators.BaseActuators.BaseActuatorState import BaseActuatorState


class BuzzerState(BaseActuatorState):
    __metaclass__ = ABCMeta

    def __init__(self, led, duration=-1, returning_state=None):
        super(BuzzerState, self).__init__(led, duration, returning_state)
