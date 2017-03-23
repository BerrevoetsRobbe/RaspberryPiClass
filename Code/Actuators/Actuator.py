from abc import ABCMeta, abstractmethod
from threading import Thread


class Actuator(Thread):
    __metaclass__ = ABCMeta

    def __init__(self, state):
        super(Actuator, self).__init__()
        self.state = state
        self.__exit_flag = False

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

    def set_state(self, state):
        self.state = state

    def stop(self):
        self.__exit_flag = True

    def run(self):
        while not self.__exit_flag:
            self.state.perform_action()
        self.destroy()
