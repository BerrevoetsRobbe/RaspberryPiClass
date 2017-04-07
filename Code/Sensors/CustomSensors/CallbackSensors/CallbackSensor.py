from threading import Thread

from abc import ABCMeta, abstractmethod

import logging

from Sensors.CustomSensors.CustomSensor import CustomSensor


class CallbackSensor(CustomSensor, Thread):
    __metaclass__ = ABCMeta

    def __init__(self, callback_function):
        super(CallbackSensor, self).__init__()
        # callback function must accept one argument
        self.callback_function = callback_function or self.default_action
        self.exit_flag = False

    @abstractmethod
    def destroy(self):
        raise NotImplementedError()

    def stop(self):
        logging.info("Stopping {object}".format(object=self))
        self.exit_flag = True

    def default_action(self, value):
        pass
