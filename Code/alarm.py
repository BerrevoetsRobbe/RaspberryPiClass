import re
import logging
import sys

import zmq
import RPi.GPIO as GPIO

from argparse import ArgumentParser
from functools import partial
from time import sleep
from Actuators.BaseActuators.Buzzer import Buzzer
from Actuators.BaseActuators.Camera import Camera
from Actuators.BaseActuators.LED import LED
from Actuators.CustomActuators.MultipleLED import MultipleLED
from Alarm.Alarm import Alarm
from Sensors.BaseSensors.CallbackSensors.Keys.NumKey import NumKey
from Sensors.BaseSensors.CallbackSensors.Keys.SymbolKey import SymbolKey
from Sensors.BaseSensors.PollingSensors.LightSensor import LightSensor
from Sensors.BaseSensors.PollingSensors.ReedSensor import ReedSensor
from Sensors.CustomSensors.CallbackSensors.DoorSensor import DoorSensor
from Sensors.CustomSensors.CallbackSensors.PinPad import PinPad
from Sensors.CustomSensors.PollingSensors.ThresholdSensor import ThresholdSensor
from Server.server import Server

ADD_PATTERN = re.compile("add (?P<type>\w+) (?P<device>\w+)(?P<pin_numbers>(\s*\d+)*)")
ADD_PATTERN_NL = re.compile("voeg toe (?P<type>\w+) (?P<device>\w+)(?P<pin_numbers>(\s*\d+)*)")
PIN_PATTERN = re.compile("set pin (?P<pin>\w+)")
PIN_PATTERN_NL = re.compile("stel pin in (?P<pin>\w+)")
RESET_ALARM_PATTERN = re.compile("reset alarm")
TAKE_PICTURE_PATTERN = re.compile("take picture")
LIGHT_THRESHOLD = 0.5

alarm = None
buzzer = None
pinpad = None
camera = None
door_sensor = None
PIN = "3576"
escape_key = '*'
pipe_path = "/home/pi/tmp/alarm_pipe"


def create_key_list():
    logging.debug("start key creation")
    key_list = [NumKey(i) for i in range(1, 10)]
    key_list.append(SymbolKey('*'))
    key_list.append(NumKey(0))
    key_list.append(SymbolKey('#'))
    logging.debug("key list generated: {list}".format(list=key_list))
    return key_list


def add_actuator(device, pin_numbers):
    if device in ACTUATOR_POSSIBILITIES.keys():
        ACTUATOR_POSSIBILITIES[device](pin_numbers)
    else:
        logging.info("Wrong device given for actuators: {device}!".format(device=device))


def add_door_sensor(device, pin_numbers):
    if device in DOOR_SENSOR_POSSIBILITIES.keys():
        DOOR_SENSOR_POSSIBILITIES[device](pin_numbers)
    else:
        logging.info("Wrong device given for door sensor: {device}".format(device=device))


def add_activation_sensor(device, pin_numbers):
    if device in ACTIVATION_SENSOR_POSSIBILITIES.keys():
        ACTIVATION_SENSOR_POSSIBILITIES[device](pin_numbers)
    else:
        logging.info("Wrong device given for activation sensor: {device}".format(device=device))


def add_actuator_led(pin_numbers):
    global alarm
    if len(pin_numbers) < 2:
        logging.info("Not enough pin numbers given for LED initialisation")
        return
    led = LED(pin_numbers[0], pin_numbers[1])
    led.start()
    alarm.add_actuator(led)


def add_actuator_buzzer(pin_numbers):
    global alarm, buzzer
    if len(pin_numbers) < 1:
        logging.info("Not enough pin numbers given for buzzer initialisation")
        return
    buzzer = Buzzer(pin_numbers[0])
    buzzer.start()
    alarm.add_actuator(buzzer)


def add_actuator_multiple_led(pin_numbers):
    global alarm
    if len(pin_numbers) % 2 != 0:
        logging.info("Not enough pin numbers given for multiple led initialisation")
        return
    leds = [LED(pin_numbers[i], pin_numbers[i + 1]) for i in range(0, len(pin_numbers), 2)]
    for led in leds:
        led.start()

    multiple_led = MultipleLED(leds)
    multiple_led.start()
    alarm.add_actuator(multiple_led)


def add_actuator_camera(_):
    global alarm, camera
    camera = Camera()
    alarm.add_actuator(camera)


def add_door_sensor_light_sensor(pin_numbers):
    global alarm, door_sensor
    if len(pin_numbers) < 1:
        logging.info("Not enough pin numbers given for light sensor initialisation")
        return
    light_sensor = LightSensor(pin_numbers[0])
    threshold_sensor = ThresholdSensor(light_sensor, LIGHT_THRESHOLD)
    door_sensor = DoorSensor(threshold_sensor, 1, 0,  partial(Alarm.callback_door, alarm))
    door_sensor.start()


def add_door_sensor_reed_switch(pin_numbers):
    global alarm, door_sensor
    if len(pin_numbers) < 1:
        logging.info("Not enough pin numbers given for reed sensor initialisation")
        return
    reed_sensor = ReedSensor(pin_numbers[0])
    door_sensor = DoorSensor(reed_sensor, 1, 0, partial(Alarm.callback_door, alarm))
    door_sensor.start()


def add_activation_sensor_pinpad(pin_numbers):
    global alarm, pinpad, PIN, escape_key, buzzer
    if len(pin_numbers) < 7:
        logging.info("Not enough pin numbers given for pinpad initialisation")
        return
    keys = create_key_list()
    pinpad = PinPad(pin_numbers[0:4], pin_numbers[4:7], keys, PIN, escape_key, buzzer,
                    callback_function=partial(Alarm.callback_activation, alarm))
    pinpad.start()


def set_pin(pin):
    global pinpad
    if pinpad:
        pinpad.set_pin(pin)
    else:
        logging.info("Pinpad must first be added")


def reset_alarm():
    global alarm, door_sensor, pinpad
    logging.info("Resetting alarm")
    if alarm:
        alarm.stop()
    if door_sensor:
        door_sensor.stop()
    if pinpad:
        pinpad.stop()
    sleep(1)
    alarm = Alarm()
    alarm.start()

DEVICE_TYPES = dict(
    ACTUATOR=add_actuator,
    DOOR_SENSOR=add_door_sensor,
    ACTIVATION_SENSOR=add_activation_sensor,
)

ACTUATOR_POSSIBILITIES = dict(
    LED=add_actuator_led,
    BUZZER=add_actuator_buzzer,
    MULTIPLE_LED=add_actuator_multiple_led,
    CAMERA=add_actuator_camera,
)

DOOR_SENSOR_POSSIBILITIES = dict(
    LIGHT_SENSOR=add_door_sensor_light_sensor,
    REED_SWITCH=add_door_sensor_reed_switch,
)


ACTIVATION_SENSOR_POSSIBILITIES = dict(
    PINPAD=add_activation_sensor_pinpad,
)

def parse_arguments():
    parser = ArgumentParser(description='test different elements')
    parser.add_argument('-l', '--log', help='indicates the level of logging (INFO, DEBUG)')
    parser.add_argument('-f', '--file', help='write to logs to this file')
    args = parser.parse_args()
    setup_logger(args.log, args.file)

    logging.debug("Arguments supplied to testing are: {args}".format(args=args))


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


def take_picture():
    global camera
    if camera:
        camera.take_picture()


def perform_action(message):
    matched = False
    match = ADD_PATTERN.match(message)
    if match and match.group('type').upper() in DEVICE_TYPES.keys():
        logging.info("adding Actuator with type {type}"
                     " and pin numbers {pin_numbers}.".format(type=match.group('type').upper(),
                                                              pin_numbers=match.group('pin_numbers')))
        _type = match.group('type').upper()
        device = match.group('device').upper()
        if match.group('pin_numbers'):
            pin_numbers = [int(i) for i in match.group('pin_numbers')[1:].split(' ')]
        else:
            pin_numbers = []
        DEVICE_TYPES[_type](device, pin_numbers)
        matched = True
    match = ADD_PATTERN_NL.match(message)
    if match and match.group('type').upper() in DEVICE_TYPES.keys():
        logging.info("adding Actuator with type {type}"
                     " and pin numbers {pin_numbers}.".format(type=match.group('type').upper(),
                                                              pin_numbers=match.group('pin_numbers')))
        _type = match.group('type').upper()
        device = match.group('device').upper()
        if match.group('pin_numbers'):
            pin_numbers = [int(i) for i in match.group('pin_numbers')[1:].split(' ')]
        else:
            pin_numbers = []
        DEVICE_TYPES[_type](device, pin_numbers)
        matched = True
    match = PIN_PATTERN.match(message)
    if match:
        set_pin(match.group('pin'))
        matched = True
    match = PIN_PATTERN_NL.match(message)
    if match:
        set_pin(match.group('pin'))
        matched = True
    match = RESET_ALARM_PATTERN.match(message)
    if match:
        reset_alarm()
        matched = True
    match = TAKE_PICTURE_PATTERN.match(message)
    if match:
        matched = True
        take_picture()
    if not matched:
        logging.info("wrong command given: {command}".format(command=message))

context = zmq.Context()
server = context.socket(zmq.REP)
server.connect("tcp://0.0.0.0:5555")

parse_arguments()

http_server = Server(8080)
http_server.start()

try:
    global alarm
    GPIO.setmode(GPIO.BCM)
    alarm = Alarm()
    alarm.start()
    logging.info("Alarm started")
    while True:
        message = server.recv_string()
        if message:
            logging.info('received command "{message}"'.format(message=message))
            logging.warning('Commando "{message} ontvangen"'.format(message=message))
            try:
                perform_action(message)
                logging.info('performed command "{message}"'.format(message=message))
                logging.warning('Commando "{message}" uitgevoerd'.format(message=message))
                server.send_string('commando "{message}" uitgevoerd'.format(message=message))
            except:
                logging.warning('Er is een fout opgetreden, kan commando "{message}" niet uitvoeren'.format(message=message))
                server.send_string('Er is een fout opgetreden, kan commando "{message}" niet uitvoeren'.format(message=message))
            alarm.refresh()
            sleep(0.5)
except KeyboardInterrupt:
    reset_alarm()
    http_server.cleanup()
    alarm.stop()
    sleep(1)
    GPIO.cleanup()
    sys.exit(0)
