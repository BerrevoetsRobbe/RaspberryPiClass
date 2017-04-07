from unittest import TestCase
from Alarm.Alarm import Alarm
from Alarm.AlarmState.AlarmState import AlarmState
from Alarm.AlarmState.Activated import Activated
from Alarm.AlarmState.Triggered import Triggered


class TestIdle(TestCase):

    def setUp(self):
        self.alarm = Alarm()
        self.idle = self.alarm.get_alarm_state()

    def test_door_state(self):
        self.assertEqual(self.idle.get_door_state(), AlarmState.DOOR_CLOSED)

        self.idle.door_opened()

        self.assertEqual(self.idle.get_door_state(), AlarmState.DOOR_OPEN)

        self.idle.door_closed()

        self.assertEqual(self.idle.get_door_state(), AlarmState.DOOR_CLOSED)

    def test_alarm_activated_door_closed(self):
        self.assertEqual(self.idle.get_door_state(), AlarmState.DOOR_CLOSED)

        self.idle.alarm_activated()

        self.assertIsInstance(self.alarm.get_alarm_state(), Activated)
        self.assertFalse(self.alarm.get_alarm_state().is_door_open())

    def test_alarm_activated_door_open(self):
        self.idle.door_opened()
        self.assertEqual(self.idle.get_door_state(), AlarmState.DOOR_OPEN)

        self.idle.alarm_activated()

        self.assertIsInstance(self.alarm.get_alarm_state(), Triggered)
        self.assertTrue(self.alarm.get_alarm_state().is_door_open())
