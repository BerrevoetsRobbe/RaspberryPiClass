from abc import ABCMeta, abstractmethod


class Key(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_value(self):
        raise NotImplementedError()