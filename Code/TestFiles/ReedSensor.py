import RPi.GPIO as GPIO

from time import sleep
from Actuators.BaseActuators.LED import LED
from Sensors.BaseSensors.PollingSensors.ReedSensor import ReedSensor


def test_reed_sensor(args):
    reed_sensor = ReedSensor(int(args[0]))
    led = LED(int(args[1]), int(args[2]))

    try:
        while True:
            if reed_sensor.get_value() == 0:
                led.perform_action_activated()
                sleep(0.000001)
            if reed_sensor.get_value() == 1:
                led.perform_action_idle()
                sleep(0.000001)

    finally:
        led.destroy()
        reed_sensor.destroy()
        sleep(0.5)
        GPIO.cleanup()
