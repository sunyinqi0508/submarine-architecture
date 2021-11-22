from random import randint
from client_abstract_class import Player

HOST = '127.0.0.1'
PORT = 5005
NAME = 'Python Submarine Client'

class SubmarineCaptain(Player):
    def __init__(self, name = NAME, host = HOST, port = PORT):
        super().__init__(host, port, name)
        game_info = self.recv()
        print('submarine info:', game_info)
        self.m = game_info['m']
        self.L = game_info['L']
        self.position = game_info['position']

    def play_game(self):
        response = {'terminated': False, 'probed': False} #initial state
        while not response['terminated']:
            move = self.your_algorithm(response['probed'])
            self.send({"movement": move})
            self.position += move
            response = self.recv()
            print(response)
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

if __name__ == '__main__':
    SubmarineCaptain().play_game()