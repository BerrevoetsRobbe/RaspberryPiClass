from BaseActuator import BaseActuator
from picamera import PiCamera
import logging

logger = logging.getLogger(__name__)


class Camera(BaseActuator):

    def __init__(self):
        super(Camera, self).__init__()
        self.__camera = PiCamera()
        self.__counter = 0

    def perform_action_idle(self):
        logger.debug("Camera performing idle action")

    def perform_action_activated(self):
        logger.debug("Camera performing activated action")

    def perform_action_triggered(self):
        logger.debug("Camera performing triggered action")
        self.__take_picture()

    def __take_picture(self):
        self.__camera.capture('image_{counter}.jpg'.format(counter=self.__counter))

    def destroy(self):
        logger.debug("Camera cleanup")
        self.__camera.close()
