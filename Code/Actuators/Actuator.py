from abc import ABCMeta, abstractmethod


class Actuator(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def perform_action_idle(self):
        raise NotImplementedError()

    @abstractmethod
    def perform_action_triggered(self):
        raise NotImplementedError()

    @abstractmethod
    def perform_action_activated(self):
        raise NotImplementedError()

    @abstractmethod
    def destroy(self):
        raise NotImplementedError()
