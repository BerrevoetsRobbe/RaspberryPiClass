from abc import ABCMeta, abstractmethod


class Sensor(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def destroy(self):
        raise NotImplementedError()
