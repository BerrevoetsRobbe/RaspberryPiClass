from time import sleep

from Actuators.BaseActuators.LED import LED
from Actuators.BaseActuators.LEDStates.Green import Green
from Actuators.BaseActuators.LEDStates.Red import Red
from Sensors.BaseSensors.PollingSensors.LightSensor import LightSensor
from Sensors.CustomSensors.PollingSensors.ThresholdSensor import ThresholdSensor

led = None
THRESHOLD_VALUE = 0.5  # TODO: determine value


def callback_above():
    global led
    if led:
        led.set_state(Red(led, returning_state=led.state))


def callback_below():
    global led
    if led:
        led.set_state(Green(led, returning_state=led.state))


def test_threshold_sensor(args):
    light_sensor = LightSensor(int(args[0]))
    global led
    led = LED(int(args[1]), int(args[2]))
    led.start()
    threshold_sensor = ThresholdSensor(light_sensor, THRESHOLD_VALUE, callback_below, callback_above)
    threshold_sensor.start()
    try:
        while True:
            sleep(0.000001)
    finally:
        threshold_sensor.destroy()
