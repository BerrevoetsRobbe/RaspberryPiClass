#!/usr/bin/env python

from Actuators.BaseActuators.Camera import Camera
from time import time, sleep

IDLE_TIME = 5
ACTIVATION_TIME = 5
TRIGGERED_TIME = 5


def test_general(camera):
    camera.perform_action_idle()
    camera.perform_action_activated()
    camera.perform_action_triggered()


def test_camera(_):
    camera = Camera()
    camera.start()
    try:
        start_time = time()
        camera.perform_action_idle()
        while start_time + IDLE_TIME > time():
            # yield processor
            sleep(0.000001)
        camera.perform_action_activated()
        while start_time + IDLE_TIME + ACTIVATION_TIME > time():
            # yield processor
            sleep(0.000001)
        camera.perform_action_triggered(10)
        while True:
            # yield processor
            sleep(0.000001)
    finally:
        camera.stop()
        camera.join(2)
