import json
from random import randint

from clients.client_abstract_class import Player


class SubmarineCaptain(Player):
    def __init__(self, name):
        super(SubmarineCaptain, self).__init__(name=name, is_trench_manager=False)
        game_info = json.loads(self.client.receive_data())
        print('sub', game_info)
        self.m = game_info['m']
        self.L = game_info['L']
        self.position = game_info['pos']

    def play_game(self):
        response = {}
        while True:
            move = self.your_algorithm(0 if not response else response['times_probed'])
            self.client.send_data(json.dumps({"move": move}))
            self.position += move
            response = json.loads(self.client.receive_data())
            if 'game_over' in response:
                print(f"The trench manager's final cost is: {response['trench_cost']}. " +
                      f"The safety condition {'was' if response['was_condition_achieved'] else 'was not'} satisfied.")
                exit(0)
            self.m -= 1

    def your_algorithm(self, times_probed):
        """
        PLACE YOUR ALGORITHM HERE

        As the submarine captain, you only ever have access to your position (self.position),
        the amount of times you were successfully probed (times_probed), how long is the game
        (self.m), and the range of the probes(self.L).

        You must return an integer between [-1, 1]
        """
        return randint(-1, 1)