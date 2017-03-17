from unittest import TestCase
from Alarm.Alarm import Alarm
from Alarm.AlarmState.AlarmState import AlarmState
from Alarm.AlarmState.Activated import Activated
from Alarm.AlarmState.Triggered import Triggered
from Alarm.AlarmState.Idle import Idle


class TestActivated(TestCase):

    def setUp(self):
        self.alarm = Alarm([], None, None)
        self.activated = Activated(self.alarm, [], AlarmState.DOOR_CLOSED)
        self.alarm.set_alarm_state(self.activated)

    def test_door_opened(self):
        self.assertEqual(self.activated.get_door_state(), AlarmState.DOOR_CLOSED)

        self.activated.door_opened()

        self.assertEqual(self.activated.get_door_state(), AlarmState.DOOR_OPEN)

        self.assertIsInstance(self.alarm.get_alarm_state(), Triggered)
        self.assertTrue(self.alarm.get_alarm_state().is_door_open())

    def test_door_closed(self):
        self.assertEqual(self.activated.get_door_state(), AlarmState.DOOR_CLOSED)

        self.activated.door_opened()
        self.activated.door_closed()

        self.assertEqual(self.activated.get_door_state(), AlarmState.DOOR_CLOSED)

    def test_alarm_deactivated(self):
        self.assertEqual(self.activated.get_door_state(), AlarmState.DOOR_CLOSED)

        self.activated.alarm_deactivated()

        self.assertIsInstance(self.alarm.get_alarm_state(), Idle)
