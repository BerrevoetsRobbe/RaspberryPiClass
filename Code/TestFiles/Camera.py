#!/usr/bin/env python

from Actuators.BaseActuators.Camera import Camera


def test_general(camera):
    camera.perform_action_idle()
    camera.perform_action_activated()
    camera.perform_action_triggered()


def test_camera(_):
    camera = Camera()
    try:
        test_general(camera)
    finally:
        camera.destroy()
