"""Class to handle log parsing from game state."""

import json


class LogParser:
    """Log Parser class to read and extract information from game state."""

    def __init__(self, file_name) -> None:
        """Initialise class using log file name."""
        self.file_name = file_name
        self.parent_types = [
            r"CubeGame.Location, SecondDinner.CubeGame.Logic",
            r"CubeGame.Player, SecondDinner.CubeGame.Logic",
        ]
        self.child_types = [
            r"CubeGame.CardStaged, SecondDinner.CubeGame.Logic" r"CubeGame.Card, SecondDinner.CubeGame.Logic",
        ]
        self.hand_type = r"CubeGame.Hand, SecondDinner.CubeGame.Logic"

    def extract_state(self, game_type="remote"):
        """Extracts state information into JSON document.

        Used to extract the actual objects and removes refs
        """
        with open(self.file_name, "r", encoding="utf-8-sig") as file:
            state_file = json.load(file)
            if game_type == "remote":
                return self.extract_remote_game(state_file["RemoteGame"])
            else:
                raise NotImplementedError("Non remote game state is not curently implemented")

    def extract_remote_game(self, remote_game_json: dict) -> dict:
        """Extacts state from the remote game section."""
        final_state = {}
        # Extract State Information
        if not remote_game_json["ClientPlayerInfo"]["CardsDrawn"]:
            return final_state
        game_state = remote_game_json["GameState"]

        final_state["state"] = {
            "current_turn": game_state["Turn"],
            "current_cubes": game_state["CubeValue"],
            "next_turn_cubes": game_state["CubeValueNextTurn"],
        }
        if "ClientResultMessage" in game_state:
            # Assumption is first result is player needs to be validated
            final_state["result"] = {
                "winner": game_state["ClientResultMessage"]["GameResultAccountItems"][0]["IsWinner"],
                "cubes_traded": game_state["ClientResultMessage"]["FinalCubeValue"],
            }

        # Remove Pre Start turn so we have a single view
        # Extract Location Information
        game_state.pop("GameAtPreStartTurn")
        for extract in self.extract_parent_ids(game_state):
            if "Player" in extract[r"$type"]:
                if game_state["Players"][0][r"$id"] == extract[r"$id"]:
                    player_id = 1
                else:
                    player_id = 2
                final_state[f"player_{player_id}"] = {
                    "hand": extract["Hand"]
                    if r"$id" in extract["Hand"]
                    else self.extract_specific_ids(game_state, extract["Hand"][r"$ref"], self.hand_type),
                    "deck": extract["Deck"]
                    if r"$id" in extract["Deck"]
                    else self.extract_specific_ids(game_state, extract["Deck"][r"$ref"], self.hand_type),
                    "current_energy": extract.get("CurrentEnergy", extract.get("MaxEnergy", None)),
                    "has_snapped": None,  # Need to find how this is stored
                }
            elif "Location" in extract[r"$type"]:
                if "location" not in final_state:
                    final_state["location"] = {}
                final_state["location"][extract.get("SlotIndex", 3)] = {
                    "player_1_cards": extract["Player1Cards"],
                    "player_2_cards": extract["Player2Cards"],
                }
                pass
            else:
                NotImplementedError(f'The following {extract[r"type"]} has not been implemented')
        return final_state

    def monitor_for_changes(self):
        """To-Do."""
        pass

    def extract_parent_ids(self, state: any, result=None):
        """Recursively extracts ID objects from game state."""
        if result is None:
            result = []

        if isinstance(state, dict):
            if r"$id" in state:
                if r"$type" in state and state[r"$type"] in self.parent_types:
                    result.append(state)
            for _key, value in state.items():
                self.extract_parent_ids(value, result)
        elif isinstance(state, list):
            for x in state:
                self.extract_parent_ids(x, result)

        return result

    def extract_specific_ids(self, state: any, obj_id, obj_type, result=None):
        """Recursively extracts ID objects from game state."""
        if isinstance(state, dict):
            if r"$id" in state:
                # print(state)
                if r"$type" in state and state[r"$type"] == obj_type and state["$id"] == obj_id:
                    return state
            for _key, value in state.items():
                result = self.extract_specific_ids(value, obj_id, obj_type)
                if result is not None:
                    return result
        elif isinstance(state, list):
            for x in state:
                result = self.extract_specific_ids(x, obj_id, obj_type)
                if result is not None:
                    return result
