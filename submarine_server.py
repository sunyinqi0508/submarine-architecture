import json
from random import randint
from time import time

from hps.servers import SocketServer
from websocket_server import WebsocketServer

HOST = '127.0.0.1'
PORT = 5000

WEB_HOST = '127.0.0.1'
WEB_PORT = 8000

class GameServer(object):
    def __init__(self, d=36, y=6, r=6, m=10, L=4, p=2, gui=False):
        self.d = d
        self.y = y
        self.r = r
        self.m = m
        self.L = L
        self.p = p
        self.trench_cost = 0
        self.trench_condition_achieved = True
        self.red_alert = [i % 100 for i in range(d, d+6)]
        self.submarine_time_left = self.trench_time_left = 120
        self.submarine_location = randint(0, 99)
        self.is_submarine_in_red = self.submarine_location in self.red_alert
        self.web_server = None
        print('Waiting on port %s for players...' % PORT)
        if gui:
            self.web_server = WebsocketServer(WEB_PORT, host=WEB_HOST)
            self.web_server.new_client = self.accept_player_connections
            self.web_server.run_forever()
        else:
            self.accept_player_connections()


    def accept_player_connections(self, front_end=None, web_server=None):
        if front_end:
            print('~~ WE GOT A FRONT END ~~')
        self.server = SocketServer(HOST, PORT, 2)
        self.server.establish_client_connections()
        self.player_attributes = [json.loads(info) for info in self.server.receive_from_all()]
        self.trench_idx = 0 if self.player_attributes[0]['is_trench_manager'] else 1
        self.submarine_idx = 1 if self.player_attributes[0]['is_trench_manager'] else 0
        self.play_game()


    def timed_request(self, request_data, client_idx):
        self.server.send_to(json.dumps(request_data), client_idx)
        start = time()
        move = json.loads(self.server.receive_from(client_idx))
        stop = time()
        return move, (stop - start)


    def decrement_time(self, submarine_time_spent, trench_time_spent):
        self.submarine_time_left -= submarine_time_spent
        self.trench_time_left -= trench_time_spent


    def check_time_left(self):
        if self.submarine_time_left < 0:
            raise Exception('Submarine Captain ran out of time')

        if self.trench_time_left < 0:
            raise Exception('Trench Manager ran out of time')


    def complete_submarine_move(self, submarine_move):
        if type(submarine_move) != int or submarine_move > 1 or submarine_move < -1:
            raise ValueError('Submarine Captain made an illegal move')

        self.submarine_location = (self.submarine_location + submarine_move) % 100
        self.is_submarine_in_red = self.submarine_location in self.red_alert


    def trench_region_check(self, region):
        if region not in ('red', 'yellow'):
            raise ValueError('Trench Manager chose an illegal region')

        if self.is_submarine_in_red and region != 'red':
            self.trench_condition_achieved = False

        self.trench_cost += self.r if region == 'red' else self.y


    def deploy_probes(self, probes):
        probe_results = []
        times_submarine_probed = 0
        for probe in probes:
            if type(probe) != int or probe < 0 or probe > 99:
                raise ValueError('Trench Manager placed a probe at an illegal position')

            range_start = (probe - self.L) if (probe - self.L) > 0 else (100 + (probe - self.L))
            probe_range = [i % 100 for i in range(range_start, range_start + (self.L * 2) + 1)]

            probe_results.append(self.submarine_location in probe_range)
            if probe_results[-1]:
                times_submarine_probed += 1
            self.trench_cost += self.p
        return probe_results, times_submarine_probed


    def play_game(self):
        submarine_move, submarine_time_spent = self.timed_request(
            {'m': self.m, 'L': self.L, 'pos': self.submarine_location},
            self.submarine_idx
        )

        trench_probe_move, trench_time_spent = self.timed_request(
            {'d': self.d, 'y': self.y, 'r': self.r, 'm': self.m, 'L': self.L, 'p': self.p},
            self.trench_idx
        )

        self.decrement_time(submarine_time_spent, trench_time_spent)

        m = self.m
        while m > 0:
            self.check_time_left()

            self.complete_submarine_move(submarine_move['move'])

            probe_results, times_submarine_probed = self.deploy_probes(trench_probe_move['probes'])

            trench_move, trench_time_spent = self.timed_request(
                {'probe_results': probe_results},
                self.trench_idx
            )

            self.trench_region_check(trench_move['region'])

            if self.web_server:
                self.web_server.send_message_to_all(json.dumps({
                    'red_region': self.d,
                    'position': self.submarine_location,
                    'is_safety_condition_achieved': self.trench_condition_achieved,
                    'submarine_region': 'red' if self.is_submarine_in_red else 'yellow',
                    'trench_alert': trench_move['region'],
                    'probes': trench_probe_move['probes']
                }))

            print("**********************************************")
            print(f"Submarine moved by {submarine_move['move']} (current position: {self.submarine_location})")
            print(f"Submarine is {'not' if not self.is_submarine_in_red else ''} in red region")
            print(f"Probes were placed at {trench_probe_move['probes']}")
            print(f"The results were: {probe_results}")
            print(f"Trench manager sent {trench_move['region']} alert")
            print(f"Safety condition {'not' if not self.trench_condition_achieved else ''} achieved")
            print("**********************************************")

            if m > 1:
                submarine_move, submarine_time_spent = self.timed_request(
                    {'times_probed': times_submarine_probed},
                    self.submarine_idx
                )

                trench_probe_move, trench_time_spent = self.timed_request(
                    {},
                    self.trench_idx
                )

                self.decrement_time(submarine_time_spent, trench_time_spent)

            m -= 1

        if not self.trench_condition_achieved:
            self.trench_cost = (self.m * self.r) + (self.m * 5 * self.p)

        self.server.send_to_all(
            json.dumps({
                'game_over': True,
                'trench_cost': self.trench_cost,
                'was_condition_achieved': self.trench_condition_achieved
            })
        )
