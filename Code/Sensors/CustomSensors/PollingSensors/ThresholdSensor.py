from Sensors.CustomSensors.PollingSensors.PollingSensor import PollingSensor


class ThresholdSensor(PollingSensor):

    def __init__(self, base_sensor, threshold):
        super(ThresholdSensor, self).__init__()
        self.__base_sensor = base_sensor
        self.__threshold = threshold

    def get_value(self):
        if self.__base_sensor.get_value() < self.__threshold:
            return 0
        else:
            return 1

    def destroy(self):
        pass
