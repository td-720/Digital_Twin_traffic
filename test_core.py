import unittest
try:
    from core import TrafficMonitor
except ImportError:
    from sensor_and_processing import TrafficMonitor

class TestTrafficSystem(unittest.TestCase):
    def setUp(self):
        self.monitor = TrafficMonitor(speed_limit=100)

    def test_overspeed_violation(self):
        # 120 is over 100, should be True
        self.assertTrue(self.monitor.check_violation(120))

    def test_normal_speed(self):
        # 80 is under 100, should be False
        self.assertFalse(self.monitor.check_violation(80))

if __name__ == '__main__':
    unittest.main()
  
