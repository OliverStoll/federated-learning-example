import socket
from random import randint
from time import sleep

from logger import log


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
clients = []


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.weights = 0

    def train(self):
        sleep(1)
        self.weights = randint(0, 20)
        # log(f'trained with new weights {self.weights}')

    def send(self):
        log(f'Send data {self.weights}')
        data = self.weights.to_bytes(1, byteorder='big')
        header = len(data).to_bytes(4, byteorder='big')
        self.socket.sendall(header)
        self.socket.sendall(data)

    def recv(self):
        data = self.socket.recv(1024)
        self.weights = int.from_bytes(data, 'big')
        log(f'Received updated weights: {self.weights}')


for i in range(3):
    clients.append(Client())
while True:
    for client in clients:
        client.train()
        client.send()
    for client in clients:
        client.recv()

