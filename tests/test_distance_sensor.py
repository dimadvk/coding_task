import unittest
from sensors import DistanceSensor


class TestDistanceSensor(unittest.TestCase):
    def setUp(self):
        self.sensor = DistanceSensor()

    def tearDown(self):
        self.sensor.control(power=False)

    def test_invalid_rate(self):
        resp = self.sensor.control(power=True, rateHz=0)
        self.assertFalse(resp["acknowledge"])
        self.assertFalse(self.sensor._power)

    def test_invalid_power(self):
        with self.assertRaises(ValueError):
            self.sensor.control(power='1', rateHz=DistanceSensor.ALLOWED_RATE_HZ[0])
        self.assertFalse(self.sensor._power)

    def test_power_on(self):
        resp = self.sensor.control(power=True, rateHz=DistanceSensor.ALLOWED_RATE_HZ[1])
        self.assertTrue(resp["acknowledge"])
        self.assertTrue(self.sensor._power)
        self.assertEqual(self.sensor._rate_hz, DistanceSensor.ALLOWED_RATE_HZ[1])

        resp = self.sensor.control(power=True, rateHz=DistanceSensor.ALLOWED_RATE_HZ[0])
        self.assertFalse(resp["acknowledge"])
        self.assertTrue(self.sensor._power)
        # if resp["acknowledge"] is False then self.sensor._rate_hz should not be updated.
        self.assertEqual(self.sensor._rate_hz, DistanceSensor.ALLOWED_RATE_HZ[1])

    def test_power_off(self):
        self.sensor.control(power=True, rateHz=DistanceSensor.ALLOWED_RATE_HZ[0])

        resp = self.sensor.control(power=False)
        self.assertTrue(resp["acknowledge"])
        self.assertFalse(self.sensor._power)

        resp = self.sensor.control(power=False)
        self.assertFalse(resp["acknowledge"])
        self.assertFalse(self.sensor._power)
