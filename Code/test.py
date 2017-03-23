import logging
import argparse
import RPi.GPIO as GPIO

from TestFiles.LED import test_led
from TestFiles.Buzzer import test_buzzer
from TestFiles.Camera import test_camera
# from TestFiles.LightSensor import test_light_sensor
from TestFiles.MultipleLED import test_multiple_led
from TestFiles.NumPad import test_num_pad
from TestFiles.PinPad import test_pin_pad
from TestFiles.ReedSensor import test_reed_sensor

# TODO: install package on Pi for photoresistor

test_func = dict(
    LED=test_led,
    BUZZER=test_buzzer,
    CAMERA=test_camera,
    # light_sensor=test_light_sensor,
    MULTIPLE_LED=test_multiple_led,
    NUM_PAD=test_num_pad,
    PIN_PAD=test_pin_pad,
    REED_SENSOR=test_reed_sensor
)


def parse_arguments():
    parser = argparse.ArgumentParser(description='test different elements')
    parser.add_argument('device', metavar='device', type=str)
    parser.add_argument('args', metavar='args', nargs='*')
    parser.add_argument('-l', '--log', help='indicates the level of logging (INFO, DEBUG)')
    parser.add_argument('-f', '--file', help='write to logs to this file')
    args = parser.parse_args()
    setup_logger(args.log, args.file)
    logging.info("Start testing")
    logging.debug("Arguments supplied to testing are: {args}".format(args=args))
    test_func[args.device.upper()](args.args)


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
    except KeyboardInterrupt:
        logging.info("Stop testing")
