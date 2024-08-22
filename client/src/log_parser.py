"""Class to handle log parsing from game state"""

import json

class LogParser:

    def __init__(self, file_name) -> None:
        self.file_name = file_name

    def extract_state(self):

        with open(self.file_name, 'r', encoding='utf-8-sig') as file:
            state_file = json.load(file)
            print(json.dumps(state_file, sort_keys=True, indent=4, default=str))
            self.extract_remote_game(state_file['RemoteGame'])


    def extract_remote_game(self, remote_game:str):
