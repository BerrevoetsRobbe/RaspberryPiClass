from Actuators.BaseActuators.CameraStates.CamaraState import CameraState


class Idle(CameraState):
    def __init__(self, camera, duration=-1, returning_state=None):
        super(Idle, self).__init__(camera, duration, returning_state)

    def return_to(self):
        pass
