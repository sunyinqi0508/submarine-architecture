import json
from random import randint, choice

from clients.client_abstract_class import Player

class TrenchManager(Player):
    def __init__(self, name):
        super(TrenchManager, self).__init__(name=name, is_trench_manager=True)
        game_info = json.loads(self.client.receive_data())
        print('trench', game_info)
        self.d = game_info['d']
        self.y = game_info['y']
        self.r = game_info['r']
        self.m = game_info['m']
        self.L = game_info['L']
        self.p = game_info['p']

    def play_game(self):
        while True:
            probes_to_send = self.send_probes()
            self.client.send_data(json.dumps({"probes": probes_to_send}))
            response = json.loads(self.client.receive_data())
            alert = self.choose_alert(probes_to_send, response['probe_results'])
            self.client.send_data(json.dumps({"region": alert}))
            response = json.loads(self.client.receive_data())
            if 'game_over' in response:
                print(f"Your final cost is: {response['trench_cost']}. " +
                      f"The safety condition {'was' if response['was_condition_achieved'] else 'was not'} satisfied.")
                exit(0)
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

        You must return one of two options: 'red' or 'yellow'
        """
        return choice(['red', 'yellow'])
