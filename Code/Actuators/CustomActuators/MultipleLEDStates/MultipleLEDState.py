from abc import ABCMeta
from Actuators.CustomActuators.CustomActuatorState import CustomActuatorState


class MultipleLEDState(CustomActuatorState):
    __metaclass__ = ABCMeta

    def __init__(self, led, duration=-1, returning_state=None):
        super(MultipleLEDState, self).__init__(led, duration, returning_state)
