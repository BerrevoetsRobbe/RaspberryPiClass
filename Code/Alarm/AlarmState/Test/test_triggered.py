import mock
import time

from unittest import TestCase
from Alarm.Alarm import Alarm
from Alarm.AlarmState.AlarmState import AlarmState
from Alarm.AlarmState.Triggered import Triggered
from Alarm.AlarmState.Idle import Idle


class TestTriggered(TestCase):

    def setUp(self):
        self.alarm = Alarm([], None, None)
        self.triggered = Triggered(self.alarm, [], AlarmState.DOOR_OPEN)
        self.alarm.set_alarm_state(self.triggered)

    def test_door_opened(self):
        self.triggered.door_closed()
        self.assertEqual(self.triggered.get_door_state(), AlarmState.DOOR_CLOSED)

        self.triggered.door_opened()

        self.assertEqual(self.triggered.get_door_state(), AlarmState.DOOR_OPEN)
        self.assertIsInstance(self.alarm.get_alarm_state(), Triggered)
        self.assertTrue(self.alarm.get_alarm_state().is_door_open())

    def test_door_closed(self):
        self.assertEqual(self.triggered.get_door_state(), AlarmState.DOOR_OPEN)

        self.triggered.door_closed()

        self.assertEqual(self.triggered.get_door_state(), AlarmState.DOOR_CLOSED)
        self.assertIsInstance(self.alarm.get_alarm_state(), Triggered)
        self.assertFalse(self.alarm.get_alarm_state().is_door_open())

    def test_alarm_deactivated_door_opened(self):
        self.assertEqual(self.triggered.get_door_state(), AlarmState.DOOR_OPEN)

        self.triggered.alarm_deactivated()

        self.assertIsInstance(self.alarm.get_alarm_state(), Idle)
        self.assertTrue(self.alarm.get_alarm_state().is_door_open())

    def test_alarm_deactivated_door_closed(self):
        self.triggered.door_closed()

        self.assertEqual(self.triggered.get_door_state(), AlarmState.DOOR_CLOSED)

        self.triggered.alarm_deactivated()

        self.assertIsInstance(self.alarm.get_alarm_state(), Idle)
        self.assertFalse(self.alarm.get_alarm_state().is_door_open())

    @mock.patch('time.time')
    def test_perform_action_time_not_exceeded(self, mock_time):
        mock_time.return_value = 0
        alarm = Alarm([], None, None)
        triggered = Triggered(alarm, [], AlarmState.DOOR_OPEN)
        alarm.set_alarm_state(triggered)

        mock_time.return_value = 20
        triggered.perform_action()

        self.assertIsInstance(alarm.get_alarm_state(), Triggered)

    @mock.patch('time.time')
    def test_perform_action_time_exceeded(self, mock_time):
        mock_time.return_value = 0
        alarm = Alarm([], None, None)
        triggered = Triggered(alarm, [], AlarmState.DOOR_OPEN)
        alarm.set_alarm_state(triggered)

        self.assertEqual(triggered.get_trigger_time(), 0)

        mock_time.return_value = 40

        self.assertEqual(time.time(), 40)
        triggered.perform_action()

        self.assertIsInstance(alarm.get_alarm_state(), Idle)
        self.assertTrue(alarm.get_alarm_state().is_door_open())
