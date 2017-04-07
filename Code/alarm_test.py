import logging
from argparse import ArgumentParser
from functools import partial
from time import sleep

import RPi.GPIO as GPIO

from Actuators.BaseActuators.Buzzer import Buzzer
from Actuators.BaseActuators.Camera import Camera
from Actuators.BaseActuators.LED import LED
from Actuators.CustomActuators.MultipleLED import MultipleLED
from Alarm.Alarm import Alarm
from Sensors.BaseSensors.CallbackSensors.Keys.NumKey import NumKey
from Sensors.BaseSensors.CallbackSensors.Keys.SymbolKey import SymbolKey
from Sensors.BaseSensors.PollingSensors.ReedSensor import ReedSensor
from Sensors.CustomSensors.CallbackSensors.DoorSensor import DoorSensor
from Sensors.CustomSensors.CallbackSensors.PinPad import PinPad

alarm = None
multiple_led = None
buzzer = None
reed_sensor = None
reed_switch = None
camera = None
pinpad = None

PIN = "5835"
escape_key = '*'


def create_key_list():
    logging.debug("start key creation")
    key_list = [NumKey(i) for i in range(1, 10)]
    key_list.append(SymbolKey('*'))
    key_list.append(NumKey(0))
    key_list.append(SymbolKey('#'))
    logging.debug("key list generated: {list}".format(list=key_list))
    return key_list


def add_multiple_led(list_of_pins):
    leds = [LED(int(list_of_pins[i]), int(list_of_pins[i + 1])) for i in range(0, len(list_of_pins), 2)]
    for led in leds:
        led.start()

    logging.debug("setting up multiple led with leds: {leds}".format(leds=leds))

    global multiple_led
    multiple_led = MultipleLED(leds)
    multiple_led.start()

    global alarm
    alarm.add_actuator(multiple_led)


def add_buzzer(buzzer_pin_list):
    global buzzer
    buzzer = Buzzer(int(buzzer_pin_list[0]))
    buzzer.start()

    global alarm
    alarm.add_actuator(buzzer)


def add_camera():
    global alarm, camera
    camera = Camera()
    alarm.add_actuator(camera)


def add_pinpad(list_of_pins):
    global buzzer, PIN, escape_key, pinpad
    row_pins = [int(arg) for arg in list_of_pins[0:4]]
    col_pins = [int(arg) for arg in list_of_pins[4:7]]
    keys = create_key_list()
    pinpad = PinPad(row_pins, col_pins, keys, PIN, escape_key, buzzer,
                    callback_function=partial(Alarm.callback_activation, alarm))
    pinpad.start()
    logging.info("created pinpad: {pinpad}".format(pinpad=pinpad))


def add_reed_sensor(reed_pin_list):
    global alarm, reed_sensor, reed_switch
    reed_sensor = ReedSensor(int(reed_pin_list[0]))
    reed_switch = DoorSensor(reed_sensor, 1, 0, partial(Alarm.callback_door, alarm))
    reed_switch.start()


def parse_arguments():
    parser = ArgumentParser(description='test different elements')
    parser.add_argument('--multiple_led', type=int, nargs='*')
    parser.add_argument('--buzzer', type=int, nargs=1)
    parser.add_argument('--pinpad', type=int, nargs='*')
    parser.add_argument('--reed_switch', type=int, nargs=1)
    parser.add_argument('-l', '--log', help='indicates the level of logging (INFO, DEBUG)')
    parser.add_argument('-f', '--file', help='write to logs to this file')
    args = parser.parse_args()
    setup_logger(args.log, args.file)

    logging.debug("Arguments supplied to testing are: {args}".format(args=args))

    global alarm
    alarm = Alarm()
    alarm.start()
    add_camera()
    add_multiple_led(args.multiple_led)
    add_buzzer(args.buzzer)
    add_pinpad(args.pinpad)
    add_reed_sensor(args.reed_switch)
    alarm.refresh()


def setup_logger(log_level=None, filename=None):
    log_level = log_level or 'WARNING'
    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    if filename:
        logging.basicConfig(filename=filename,
                            level=numeric_level,
                            format='%(asctime)s :: [%(levelname)s] :: %(filename)s :: %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')
    else:
        logging.basicConfig(level=numeric_level,
                            format='%(asctime)s :: [%(levelname)s] :: %(filename)s :: %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')

    logging.info("logger configured")


if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        parse_arguments()
        logging.info("Start alarm")
        while True:
            sleep(1)
    except KeyboardInterrupt:
        logging.info("Stop alarm")
        camera.stop()
        pinpad.stop()
        buzzer.stop()
        multiple_led.stop()
        reed_switch.stop()
        alarm.stop()
        reed_sensor.destroy()
        sleep(1)
        GPIO.cleanup()
