from BaseSensor import BaseSensor
from NumPad import NumPad
import logging

logger = logging.getLogger(__name__)


class PinPad(BaseSensor):

    def __init__(self, input_row_pins, input_column_pins, keys, pin, escape_key, buzzer):
        logging.debug("PinPad created with pin {pin} and escape_key {escape_key}".format(pin=pin,
                                                                                         escape_key=escape_key))
        self.__numpad = NumPad(input_row_pins, input_column_pins, keys, buzzer, self.register_key)
        self.__pin = [int(i) for i in str(pin)]
        self.__escape_key = escape_key
        self.__key_history = []
        self.__activated = -1

    def get_value(self):
        return self.__activated

    def register_key(self, channel):
        key = self.__numpad.detect(channel)
        if key is None:
            return
        if key.get_value() == self.__escape_key:
            logger.debug("escape key entered")
            self.__key_history = []
        else:
            self.__key_history.append(key.get_value())
            logger.debug("key {key} entered, "
                         "current key history is {key_history}".format(key=key.get_value(),
                                                                       key_history=str(self.__key_history)))

        self.__check_key_history()

    def __check_key_history(self):
        if self.__key_history == self.__pin:
            self.__pin_entered()
            self.__key_history = []

    def __pin_entered(self):
        self.__activated *= -1
        logger.info("pin entered: system is {active}active".format(active="not " if self.__activated==-1 else ""))

    def destroy(self):
        self.__numpad.destroy()
