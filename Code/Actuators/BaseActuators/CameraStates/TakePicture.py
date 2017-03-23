from Actuators.BaseActuators.CameraStates.CamaraState import CameraState


class TakePicture(CameraState):
    def __init__(self, camera, duration=-1, returning_state=None):
        super(TakePicture, self).__init__(camera, duration, returning_state)

    def perform_action(self):
        self.actuator.take_picture()
        self.actuator.set_state(self.returning_state)

    def return_to(self):
        pass
