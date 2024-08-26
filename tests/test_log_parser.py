"""Unit Tests for storing and validating Log Parser."""

import json
import unittest

from client.src import LogParser


class TestLogParser(unittest.TestCase):
    """Class to test the Log Parser Functionality on it's own."""

    REQUIRED_KEYS = ["state", "player_1", "player_2", "location"]
    FINISH_KEYS = ["result"] + REQUIRED_KEYS

    def test_parse_turn_6(self):
        """Checks Turn 6 game states and validates parses correctly."""
        file_name = "tests/fixtures/game_state_turn_6.json"
        log_parser = LogParser(file_name)

        result = log_parser.extract_state()
        self.assertCountEqual(self.FINISH_KEYS, list(result.keys()))
        self.assertEqual(3, len(result["location"].keys()))
        self.assertIn(r"$id", result["player_1"]["hand"])
        self.assertIn(r"$id", result["player_2"]["hand"])

    def test_parse_turn_4(self):
        """Checks Turn 4 game states and validates parses correctly."""
        file_name = "tests/fixtures/game_state_turn_4.json"
        log_parser = LogParser(file_name)

        result = log_parser.extract_state()
        self.assertCountEqual(self.REQUIRED_KEYS, list(result.keys()))
        self.assertEqual(3, len(result["location"].keys()))

    def test_parse_pre_game(self):
        """Checks Game State before game starts states and validates parses correctly."""
        file_name = "tests/fixtures/game_state_pre_game.json"
        log_parser = LogParser(file_name)

        result = log_parser.extract_state()
        self.assertDictEqual(result, {})

    def test_parse_ids(self):
        """Validates recursive function works as indended."""
        parser = LogParser("./tests/fixtures/game_state_turn_6.json")
        with open(parser.file_name, "r", encoding="utf-8-sig") as file:
            state_file = json.load(file)
            game_state = state_file["RemoteGame"]["GameState"]
            game_state.pop("GameAtPreStartTurn")
            result = parser.extract_parent_ids(game_state)

            self.assertEqual(5, len(result))
            self.assertEqual(3, len([location for location in result if "Location" in location[r"$type"]]))
            self.assertEqual(2, len([location for location in result if "Player" in location[r"$type"]]))

        return result


if __name__ == "__main__":
    unittest.main()
