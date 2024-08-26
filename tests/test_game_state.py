"""Unit Tests for storing and validating game state."""

import unittest

from client.src import Card, GameState, Hand, Location, Player, Turns


class TestGameState(unittest.TestCase):
    """Class to test the Game State functionality on it's own."""

    def test_parse_turn_6(self):
        """Checks Turn 6 game states and validates parses correctly."""
        file_name = "tests/fixtures/game_state_turn_6.json"
        game_state: GameState = GameState.from_log_file(file_name)

        test_turns = Turns(6, 6, 1, 2)
        player_1_hand = Hand([Card("Starlord", 2, 2), Card("TheThing", 6, 4), Card("Punisher", 3, 3)])
        test_player_1 = Player(6, 0, player_1_hand, None)
        player_2_hand = Hand(
            [
                Card("Starlord", 2, 2),
                Card("Sentinel", 3, 2),
                Card("CaptainAmerica", 3, 3),
                Card("Medusa", 2, 2),
                Card("AntMan", 1, 1),
                Card(None, -1, -1),
            ]
        )
        test_player_2 = Player(6, 0, player_2_hand, None)

        test_locations = [
            Location(
                1,
                player_1_pos=[
                    Card("MrFantastic", 2, 3),
                    Card("KaZar", 4, 4),
                    Card("AntMan", 2, 1),
                    Card("Quicksilver", 2, 1),
                ],
                player_2_pos=[
                    Card("Medusa", 5, 2),
                    Card("MrFantastic", 2, 3),
                    Card("Squirrel", 2, 1),
                ],
            ),
            Location(
                2,
                player_1_pos=[],
                player_2_pos=[Card("SquirrelGirl", 3, 1), Card("KaZar", 4, 4)],
            ),
            Location(
                3,
                player_1_pos=[
                    Card("Quicksilver", 3, 1),
                    Card("Starlord", 2, 2),
                    Card("TheThing", 6, 4),
                    Card("IronMan", -1, 5),
                ],
                player_2_pos=[
                    Card("Nightcrawler", 3, 1),
                    Card("CaptainAmerica", 3, 3),
                    Card("Squirrel", 2, 1),
                    Card("Squirrel", 8, 1),
                    Card("Squirrel", 2, 1),
                ],
            ),
        ]

        test_result = {"winner": True, "cubes_traded": 1}
        test_game_state = GameState(
            locations=test_locations,
            player_1=test_player_1,
            player_2=test_player_2,
            turns=test_turns,
            result=test_result,
        )
        test_player_2 = Player(6, 0, player_2_hand, None)
        self.assertEqual(game_state.turns, test_turns)
        self.assertEqual(game_state.player_1, test_player_1)
        self.assertEqual(game_state.player_2, test_player_2)
        self.assertEqual(game_state.result, test_result)
        self.assertEqual(game_state, test_game_state)


if __name__ == "__main__":
    unittest.main()
