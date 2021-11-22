import json
import socket
from random import randint
from time import time
import threading
from websocket_server import WebsocketServer

WEB_HOST = '127.0.0.1'
WEB_PORT = 8000
TRENCH_PORT = 5001
SUBMARINE_PORT = 5005
class GameServerCore(object):
    def __str__(self):
        return f'*** Game Configuration ***:\n\t'\
            f'd = {self.d}\n\t'\
            f'y = {self.y}\n\t'\
            f'r = {self.r}\n\t'\
            f'm = {self.m}\n\t'\
            f'L = {self.L}\n\t'\
            f'p = {self.p}\n'
    def __init__(self, d=36, y=6, r=6, m=10, L=4, p=2, gui=False, verbose = True):
        self.d = d
        self.y = y
        self.r = r
        self.m = m
        self.L = L
        self.p = p
        self.verbose = verbose
        self.probes = []
        self.submarine_probed = False
        self.red_alert = False
        self.terminated = False
        self.trench_cost = 0
        self.current_time = 0
        self.submarine_reply_lock = threading.Lock()
        self.trench_reply_lock = threading.Lock()
        self.map = [i >= d and i <= d + 5 or i <= d - 95 for i in range(100)]

        self.submarine_time_left = self.trench_time_left = 120
        self.submarine_nextlocation = self.submarine_location = randint(0, 99)
        self.trench_moved = self.submarine_moved = False
        if gui:
            self.web_server = WebsocketServer(WEB_HOST, WEB_PORT)
            self.web_server.set_fn_new_client( lambda _, s:
            s.send_message_to_all(
                json.dumps({
                        'red_region': self.d,
                        'position': self.submarine_location,
                        'is_safety_condition_achieved': False,
                        'submarine_region': 'red' if self.map[self.submarine_location] & 0x1 else 'yellow',
                        'trench_alert': 'red' if self.red_alert else 'yellow',
                        'probes': self.probes
                    })
            )
            )
            self.web_server.run_forever(threaded=True)
            
        else:
            self.web_server = None
        print(self)

    def move_n_probe(self):
        if self.submarine_moved and self.trench_moved:
            # update state, first move submarine, then probe
            self.submarine_location = self.submarine_nextlocation
            n_probes = len(self.probes)
            self.trench_cost += n_probes * self.p
            self.submarine_probed = False

            self.echos = [False] * n_probes
            for i, p in enumerate(self.probes):
                pl = p - self.L
                for pstep in range(2*self.L + 1):
                    pos = (pl + pstep) % 100
                    # self.map[pos] |= self.MAP_PROBED
                    if pos  == self.submarine_location:
                        self.echos[i] = True
                        self.submarine_probed = True
            self.trench_reply_lock.release()

    def alert(self):
        safety_condition_achieved = True
        self.trench_cost +=  self.r if self.red_alert else self.y
        if not self.red_alert and self.map[self.submarine_location] & 0x1:
            self.terminated = True
            safety_condition_achieved = False
            self.trench_cost = self.r * self.m + 5 * self.p * self.m
        self.current_time += 1
        if self.current_time >= self.m:
            self.terminated = True
        if self.submarine_time_left < 0 and self.trench_time_left < 0:
            print('Both clients are overtime.')
            self.terminated = True

        # reply all
        self.trench_moved = self.submarine_moved = False
        self.submarine_reply_lock.release()
        self.trench_reply_lock.release()
        if self.terminated:
            print("Game Terminated:", f"Time passed: {self.m}",f"Trench cost: {self.trench_cost}")
        if self.web_server:
            self.web_server.send_message_to_all(
                json.dumps({
                        'red_region': self.d,
                        'position': self.submarine_location,
                        'is_safety_condition_achieved': safety_condition_achieved,
                        'submarine_region': 'red' if self.map[self.submarine_location] & 0x1 else 'yellow',
                        'trench_alert': 'red' if self.red_alert else 'yellow',
                        'probes': self.probes
                    })
            )
        if self.verbose:
            print(f'Time {self.current_time} -> Sub location: {self.submarine_location}, ' 
                  f'Alert level: {"red" if self.red_alert else "yellow"}, '
                  f'Trench cost: {self.trench_cost}.')
            print(f'\tProbes: {self.probes}, Probe Status: {self.echos}')
            print(f'\tSubmarine Time Left: {self.submarine_time_left}, Trench Time Left: {self.trench_time_left}')

    def cb_submarine_notify(self, movement):
        self.submarine_nextlocation = (self.submarine_location + (movement > 0) - (movement < 0)) % 100
        self.submarine_moved = True
        self.move_n_probe()
    
    def cb_trench_notify(self, probes):
        self.probes = probes
        self.trench_moved = True
        self.move_n_probe()
    
class RemoteServer(object):
    def __init__(self, host, preferred_port, gameserver):
        self.current_duration = 0
        self.gameserver = gameserver
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket = None
        self.data = ''
        try:
            self.s.bind((host, preferred_port))
        except socket.error:
            self.s.bind((host, 0))
        self.port = self.s.getsockname()[1]
        self.thread = threading.Thread(target=self.run)

    def start(self):
        self.thread.start()
        
    def get_data(self):
        self.data = ''
        while True:
            d = self.client_socket.recv(4096).decode()
            self.data += d
            if len(d) < 4096:
                break
    def nop(self):
        # replace get_data with nop when this client timeouts
        pass
    def run(self):
        self.s.listen(1)
        self.client_socket, client_address = self.s.accept()
        print(f'Client accepted at {client_address}')
        self.client_socket.sendall(self.payload)
        self.current_duration = time()

        while not self.gameserver.terminated:
            self.get_data()
            self.current_duration -= time()
            self.jsondata = json.loads(self.data)
            self.lock.acquire()
            self.process_data()
            self.client_socket.sendall(self.payload)
            self.current_duration = time()

class TrenchServer(RemoteServer):
    def __init__ (self, host, gameserver):
        super().__init__(host, TRENCH_PORT,  gameserver)
        self.payload = json.dumps(
            {
                'd':gameserver.d, 
                'y':gameserver.y, 
                'r':gameserver.r, 
                'm':gameserver.m,
                'L':gameserver.L,
                'p':gameserver.p
            }
        ).encode()
        self.lock = self.gameserver.trench_reply_lock
        print(f"Starting Trench Server on port {self.port}")
        self.start()

    def process_data(self):
        self.gameserver.trench_time_left += self.current_duration
        if self.gameserver.trench_time_left > 0:
            probes = self.jsondata['probes']
            self.gameserver.cb_trench_notify(probes)
            self.lock.acquire()
            self.client_socket.sendall(json.dumps({
                'probe_results' : self.gameserver.echos,
                'time_left' : self.gameserver.trench_time_left
            }).encode())
            self.current_duration = time()
            self.get_data()
            self.gameserver.trench_time_left += self.current_duration - time()
            if self.gameserver.trench_time_left > 0:
                self.gameserver.red_alert = json.loads(self.data)['red_alert']
        else:
            probes = []
            self.get_data = self.nop
            self.gameserver.cb_trench_notify(probes)
            self.lock.acquire()
        
        self.gameserver.alert()
        self.payload = json.dumps({
            'terminated' : self.gameserver.terminated,
            'time_left' : self.gameserver.trench_time_left
        }).encode()

class SubmarineServer(RemoteServer):
    def __init__ (self, host, gameserver):
        super().__init__(host, SUBMARINE_PORT, gameserver)
        self.payload = json.dumps({
            'm':gameserver.m,
            'L':gameserver.L,
            'position' : gameserver.submarine_location
        }).encode()
        self.lock = self.gameserver.submarine_reply_lock
        print(f"Starting Submarine Server on port {self.port}")
        self.start()

    def process_data(self):
        self.gameserver.submarine_time_left += self.current_duration
        if self.gameserver.submarine_time_left > 0:
            movement = self.jsondata['movement']
            self.gameserver.cb_submarine_notify(movement)
            # probed = []
            # for i, m in enumerate(self.gameserver.map):
            #     if m & self.gameserver.MAP_PROBED:
            #         probed.append(i)
            # probed = self.gameserver.submarine_probed
            self.payload = json.dumps({
                'terminated' : self.gameserver.terminated,
                'time_left' : self.gameserver.submarine_time_left,
                'probed' : self.gameserver.submarine_probed 
            }).encode()

        else:
            self.get_data = self.nop # submarine out of time, can't move.
            self.gameserver.cb_submarine_notify(0)

if __name__ == '__main__':
    core = GameServerCore(gui=True)
    trench = TrenchServer('0.0.0.0', core)
    submarine = SubmarineServer('0.0.0.0', core)