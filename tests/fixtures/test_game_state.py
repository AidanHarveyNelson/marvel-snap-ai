import unittest

from client.src import LogParser, GameState

class TestLogParser(unittest.TestCase):


    def setUp(self):
        self.log_file = LogParser()
    def test_parse_turn_6(self):
        calculation = LogParser(8, 2)
        self.assertEqual(calculation.get_sum(), 10, 'The sum is wrong.')
