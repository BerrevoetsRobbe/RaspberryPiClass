from abc import ABCMeta
from Actuators.Actuator import Actuator


class BaseActuator(Actuator):
    __metaclass__ = ABCMeta
