import logging

from Actuators.BaseActuators.CameraStates.CamaraState import CameraState


class TakePicture(CameraState):
    def __init__(self, camera, duration=-1, returning_state=None):
        super(TakePicture, self).__init__(camera, duration, returning_state)
        self.actuator.take_picture()

    def return_to(self):
        pass
