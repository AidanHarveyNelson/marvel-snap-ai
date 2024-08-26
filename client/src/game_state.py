"""Game State Class structure."""

from .log_parser import LogParser


class Card:
    """Contains Card class."""

    def __init__(self, name, power, cost):
        """Initialise class."""
        self.name = name
        self.power = power
        self.cost = cost

    @classmethod
    def from_log_file(cls, data: dict):
        """Creates a card from Log File.

        This is useful as it will allow updating the class with more info
        and can then apply to all information later.
        """
        name = data.get("CardDefId", None)
        cost = data["Cost"].get("Value", -1)
        power = data["Power"].get("Value", -1)
        print(name)
        return cls(name, power, cost)

    def __str__(self) -> str:
        """Print's string version of object."""
        return " ".join([str(f"{key}: {var}") for key, var in vars(self).items()])

    def __eq__(self, other):
        """Comparison class."""
        if isinstance(other, Card):
            return (self.name == other.name, self.cost == other.cost, self.power == other.power)


class Location:
    """Contains Location class."""

    def __init__(self, zone_id: int, player_1_pos: list[Card], player_2_pos: list[Card]):
        """Initialise class."""
        self._zone_id = zone_id
        self.player_1_pos = player_1_pos
        self.player_2_pos = player_2_pos

    @property
    def zone_id(self):
        """Returns Zone Id."""
        return self._zone_id

    def add_to_position(self, card: Card, player: int, position: int):
        """Add's card to specific position.

        Position 1 is top left and going left to right top to bottom.
        From the lens of each player.
        |  3    4   |
        |  2    1   |
        -------------
        |  1    2   |
        |  3    4   |
        """
        if player == 1:
            self.player_1_positions[position] = card
        elif player == 2:
            self.player_2_positions[position] = card
        else:
            raise NotImplementedError("Only two players exist in the game")

    def __str__(self) -> str:
        """Print's string version of object."""
        return " ".join([str(f"{key}: {var}") for key, var in vars(self).items()])

    def __eq__(self, other):
        """Comparison class."""
        if isinstance(other, Location):
            return (
                self._zone_id == other._zone_id,
                self.player_1_pos == other.player_1_pos,
                self.player_2_pos == other.player_2_pos,
            )


class Hand:
    """Contains Hand Class."""

    def __init__(self, cards: list[Card]):
        """Initialise class."""
        self.cards = cards

    def hand_size(self):
        """Returns Hand Size."""
        return len(self.cards)

    def __str__(self) -> str:
        """Print's string version of object."""
        return f'cards: {" ".join([str(item) for item in self.cards])}]'

    def __eq__(self, other):
        """Comparison class."""
        if isinstance(other, Hand):
            return self.cards == other.cards


class Turns:
    """Contains information about turns."""

    def __init__(self, turn, max_turn, current_cubes, next_turn_cubes):
        """Initialise class."""
        self.turn = turn
        self.max_turn = max_turn
        self.current_cubes = current_cubes
        self.next_turn_cubes = next_turn_cubes

    def has_game_ended(self):
        """Checks whether game has ended."""
        if self.turn == self.max_turn:
            return True
        return False

    def __str__(self) -> str:
        """Print's string version of object."""
        return " ".join([str(f"{key}: {var}") for key, var in vars(self).items()])

    def __eq__(self, other):
        """Comparison class."""
        if isinstance(other, Turns):
            return (
                self.turn == other.turn,
                self.max_turn == other.max_turn,
                self.current_cubes == other.current_cubes,
                self.next_turn_cubes == other.next_turn_cubes,
            )


class Player:
    """Contains information about player."""

    def __init__(self, energy: int, max_energy: int, hand: Hand, has_snapped: bool):
        """Initialise player object."""
        self.energy = energy
        self.max_energy = max_energy
        self.hand = hand
        self.has_snapped = has_snapped

    def __str__(self) -> str:
        """Print's string version of object."""
        return " ".join([str(f"{key}: {var}") for key, var in vars(self).items()])

    def __eq__(self, other):
        """Comparison class."""
        if isinstance(other, Player):
            return (
                self.energy == other.energy,
                self.max_energy == other.max_energy,
                self.hand == other.hand,
                self.has_snapped == other.has_snapped,
            )


class GameState:
    """Contains information about game state."""

    def __init__(self, locations: list[Location], player_1: Player, player_2: Player, turns: Turns, result: dict):
        """Initialise key objects."""
        self.locations = locations
        self.player_1 = player_1
        self.player_2 = player_2
        self.turns = turns
        self.result = result

    @classmethod
    def from_log_file(cls, file_name: str):
        """Accepts log parser and returns game state object."""
        log_data = LogParser(file_name).extract_state("remote")
        if "state" in log_data:
            state = log_data.pop("state")
            turns = Turns(
                state["current_turn"], state.get("max_turn", 6), state["current_cubes"], state["next_turn_cubes"]
            )
        if "player_1" in log_data:
            p1 = log_data.pop("player_1")
            player_1 = Player(
                p1["current_energy"],
                p1.get("max_energy", 0),
                Hand([Card.from_log_file(card) for card in p1["hand"]["Cards"]]),
                p1["has_snapped"],
            )

        if "player_2" in log_data:
            p2 = log_data.pop("player_2")
            player_2 = Player(
                p2["current_energy"],
                p2.get("max_energy", 0),
                Hand([Card.from_log_file(card) for card in p2["hand"]["Cards"]]),
                p2["has_snapped"],
            )

        locations = []
        if "location" in log_data:
            for loc_id, value in log_data["location"].items():
                loc = Location(
                    loc_id,
                    player_1_pos=[Card.from_log_file(card) for card in value["player_1_cards"]],
                    player_2_pos=[Card.from_log_file(card) for card in value["player_2_cards"]],
                )
                locations.append(loc)

            locations.sort(key=lambda location: location.zone_id)

        result = log_data.get("result", {})
        return cls(locations, player_1, player_2, turns, result)

    def has_game_ended(self):
        """Check's whether game has ended."""
        if self.result:
            return True
        else:
            return False

    def __str__(self) -> str:
        """Print's string version of object."""
        return " ".join([str(f"{key}: {var}") for key, var in vars(self).items()])

    def __eq__(self, other):
        """Comparison class."""
        if isinstance(other, GameState):
            return (
                self.locations == other.locations,
                self.player_1 == other.player_1,
                self.player_2 == other.player_2,
                self.turns == other.turns,
                self.result == other.result,
            )
