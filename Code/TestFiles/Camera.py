#!/usr/bin/env python
import logging

from Actuators.BaseActuators.Camera import Camera
from time import time, sleep
from Server.server import Server

IDLE_TIME = 5
ACTIVATION_TIME = 5
TRIGGERED_TIME = 5


def test_general(camera):
    camera.perform_action_idle()
    camera.perform_action_activated()
    camera.perform_action_triggered()


def test_camera(_):
    http_server = Server(8080)
    http_server.start()
    camera = Camera()
    camera.start()
    logging.warning("Testen van de camera")
    try:
        camera.perform_action_triggered(10)
        while True:
            # yield processor
            sleep(0.000001)
    finally:
        camera.stop()
        camera.join(2)
        http_server.cleanup()
