"""Game State Class structure"""

from log_parser import LogParser



class Card:

    def __init__(self, id, power, cost):

        self.id = id
        self.power = power
        self.cost = cost


class Location:

    def __init__(self):

        self.positions = []

    def add_to_position(self, card: Card, position:int):
        self.positions[position] = card


class Hand:

    def __init__(self, cards:list[Card]):
        self.cards = cards


class Turns:
    def __init__(self):
        self.energy = 0
        self.max_enegy = 0
        self.turn = 0
        self.max_turn = 0


class GameState:

    def __init__(self, log_parser):

        self.log_parser = log_parser

        self.locations = Location()
        self.player_hand = Hand()
        self.enemy_hand = Hand()


        self.turns = Turns()

    def update_game_state(
            self,
            logparser: LogParser
        ):

        


        self.locations = locations
        self.player_hand = player_hand
        self.enemy_hand = enemy_hand

        self.energy = energy_cost['energy']
        self.max_enegy = energy_cost['max_energy']
        self.turn = energy_cost['turn']
        self.max_turn = energy_cost['max_turn']
