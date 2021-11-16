from random import randint, choice
from client_abstract_class import Player

HOST = '127.0.0.1'
PORT = 5001
NAME = 'Python Trench Manager Client'

class TrenchManager(Player):
    def __init__(self, name = NAME, host = HOST, port = PORT):
        super().__init__(host, port, name)
        game_info = self.recv()
        print('Trench Client Started:', game_info)
        self.d = game_info['d']
        self.y = game_info['y']
        self.r = game_info['r']
        self.m = game_info['m']
        self.L = game_info['L']
        self.p = game_info['p']

    def play_game(self):
        response = {'terminated':False, 'probe_results':[]}
        while not response['terminated']:
            probes_to_send = self.send_probes()
            self.send({"probes": probes_to_send})
            response = self.recv()
            alert = self.choose_alert(probes_to_send, response['probe_results'])
            self.send({"red_alert": alert})
            response = self.recv()
            self.m -= 1

    def send_probes(self):
        """
        PLACE YOUR PROBE ALGORITHM HERE

        As the trench manager, you have access to the start of the red alert region (self.d),
        the cost for yellow alerts (self.y), the cost for red alerts (self.r), how long is
        the game (self.m), the range of the probes (self.L), and the cost to deploy a probe (self.p)

        For this function, you must return an array of integers between 0 and 99 determining the
        location you would like to send the probes
        """
        return [randint(0,99), randint(0,99), randint(0,99)]

    def choose_alert(self, sent_probes, results):
        """
        PLACE YOUR ALERT-CHOOSING ALGORITHM HERE

        This function has access to the probes you just sent and the results. They look like:

        sent_probes: [x, y, z]
        results: [True, False, False]

        This means that deploying the probe x returned True, y returned False, and z returned False

        You must return whether or not the alert level is red alert for current time
        """
        return choice([True, False])

if __name__ == '__main__':
    TrenchManager().play_game()