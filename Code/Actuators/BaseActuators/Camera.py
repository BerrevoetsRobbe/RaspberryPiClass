from Actuators.BaseActuators.CameraStates.TakePicture import TakePicture
from Actuators.BaseActuators.CameraStates.Idle import Idle
from Actuators.BaseActuators.BaseActuator import BaseActuator
from picamera import PiCamera
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Camera(BaseActuator):

    def __init__(self):
        super(Camera, self).__init__(None)
        self.__camera = PiCamera()
        self.__counter = 0
        self.set_state(Idle(self))

    def perform_action_idle(self, duration=-1):
        logger.debug("Camera performing idle action")
        self.set_state(Idle(self, duration=duration, returning_state=self.state))

    def perform_action_activated(self, duration=-1):
        logger.debug("Camera performing activated action")
        self.set_state(Idle(self, duration=duration, returning_state=self.state))

    def perform_action_triggered(self, duration=-1):
        logger.debug("Camera performing triggered action")
        self.set_state(TakePicture(self, duration=duration, returning_state=self.state))

    def take_picture(self):
        self.__camera.capture('Images/image_{counter}_{date}.jpg'.format(counter=self.__counter,
                                                                  date=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
        self.__counter += 1

    def destroy(self):
        logger.info("Camera cleanup")
        self.__camera.close()
