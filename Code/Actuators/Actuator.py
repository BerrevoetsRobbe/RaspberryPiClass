from abc import ABCMeta, abstractmethod
from threading import Thread


class Actuator(Thread):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Actuator, self).__init__()

    @abstractmethod
    def perform_action_idle(self, duration=-1):
        raise NotImplementedError()

    @abstractmethod
    def perform_action_triggered(self, duration=-1):
        raise NotImplementedError()

    @abstractmethod
    def perform_action_activated(self, duration=-1):
        raise NotImplementedError()

    @abstractmethod
    def destroy(self):
        raise NotImplementedError()
