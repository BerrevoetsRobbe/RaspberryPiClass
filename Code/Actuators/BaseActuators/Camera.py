import logging

from datetime import datetime
from picamera import PiCamera
from picamera.array import PiRGBArray
from Actuators.BaseActuators.BaseActuator import BaseActuator
from Actuators.BaseActuators.CameraStates.Idle import Idle
from Actuators.BaseActuators.CameraStates.TakePicture import TakePicture

logger = logging.getLogger(__name__)
instance = None


class Camera(BaseActuator):

    WIDTH=480
    HEIGHT=360

    def __init__(self):
        super(Camera, self).__init__(None)
        self.__last_image = None
        self.__camera = PiCamera()
        self.__stream = PiRGBArray(self.__camera, size=(self.WIDTH, self.HEIGHT))
        self.__encoding_options = [int(cv2.cv.CV_IMWRITE_JPEG_QUALITY), 50]
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
        logging.warning("Camera neemt foto")
        self.__stream.seek(0)
        file_name = 'Images/image_{counter}_{date}.jpg'.format(counter=self.__counter,
                                                                   date=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.__camera.capture(file_name)
        self.__camera.capture(self.__stream, format='jpeg', use_video_port=True, resize=(self.WIDTH, self.HEIGHT))
        self.__counter += 1
        self.__last_image = self.__stream.array

    def get_last_image(self):
        return self.__last_image

    def destroy(self):
        global instance
        logger.info("Camera cleanup")
        instance = None
        self.__camera.close()
        self.__stream.close()

    def get_last_image_jpg(self):
        if self.__last_image is not None:
            return self.__last_image
            # result, image = cv2.imencode('.jpg', self.__last_image, self.__encoding_options)
            # if result:
            #    return image
        return None

    @staticmethod
    def get_instance():
        global instance
        return instance
