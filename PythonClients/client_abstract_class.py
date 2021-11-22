import json
import socket

class Player(object):
    def __init__(self, host, port, name):
        self.name = name
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while True:
            try:
                self.s.connect((host, port))
                break
            except:
                continue
    
    def send(self, msg):
        self.s.sendall(json.dumps(msg).encode())
    
    def recv(self):
        data = ''
        while True:
            d = self.s.recv(4096)
            data += d.decode()
            if len(d) < 4096:
                break
        return json.loads(data)