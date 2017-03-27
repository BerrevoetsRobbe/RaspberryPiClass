import logging

from Sensors.BaseSensors.CallbackSensors.NumPad import NumPad
from Sensors.CustomSensors.CallbackSensors.CallbackSensor import CallbackSensor

logger = logging.getLogger(__name__)


class PinPad(CallbackSensor):

    def __init__(self, input_row_pins, input_column_pins, keys, pin, escape_key, buzzer, callback_function=None):
        super(PinPad, self).__init__(callback_function)
        logging.debug("PinPad created with pin {pin} and escape_key {escape_key}".format(pin=pin,
                                                                                         escape_key=escape_key))
        self.__numpad = NumPad(input_row_pins, input_column_pins, keys, buzzer, self.register_key)
        self.__numpad.start()
        self.__pin = [int(i) for i in str(pin)]
        self.__escape_key = escape_key
        self.__key_history = []
        self.__activated = -1

    def get_value(self):
        return self.__activated

    def register_key(self, key):
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
        logger.info("pin entered: system is now {active}active".format(active="not " if self.__activated == -1 else ""))
        self.callback_function(self.__activated)

    def destroy(self):
        self.__numpad.stop()
