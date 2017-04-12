from time import sleep

import logging

from Sensors.CustomSensors.CallbackSensors.CallbackSensor import CallbackSensor


class DoorSensor(CallbackSensor):

    def __init__(self, sensor, open_value, closed_value, callback_function, open=False):
        super(DoorSensor, self).__init__(callback_function)
        self.__sensor = sensor
        self.__open_value = open_value
        self.__closed_value = closed_value
        self.__open = open

    def run(self):
        while not self.exit_flag:
            if self.__open and self.__sensor.get_value() == self.__closed_value:
                self.__open = False
                self.callback_function(self.__open)
                logging.info("Door closed")
                logging.warning("De deur is gesloten")
            elif not self.__open and self.__sensor.get_value() == self.__open_value:
                self.__open = True
                self.callback_function(self.__open)
                logging.info("Door opened")
                logging.warning("De deur is open")
            sleep(0.000001)
        self.destroy()

    def destroy(self):
        logging.info("DoorSensor cleanup")
        pass