import socket
import struct
import ipfsapi
import os

from logger import log

HEADER_LEN = 4


class AggClient:
    def __init__(self, socket, addr, id):
        self.socket = socket
        self.addr = addr
        self.weights = 0
        self.id = id


class Server:
    def __init__(self, host='127.0.0.1', port=65432, exit_round=3, participants=3):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()
        log('SERVER INITIALIZED')
        self.host = host
        self.port = port
        self.listener = s
        self.current_round = 1
        self.exit_round = exit_round
        self.next_id = 0
        self.clients = []
        self.participants = participants
        self.aggregated_weights = None
        self.ipfs_client = ipfsapi.Client(host='https://ipfs.infura.io', port=5001)
        self.hash = None

    def start(self):
        while len(self.clients) < self.participants:
            self.accept_client()
        while self.current_round <= self.exit_round:
            log(f'STARTING ROUND {self.current_round}')
            self.recv_all_weights()
            self.aggregate()
            self.send_all_weights()
            self.current_round += 1

    def accept_client(self):
        c_socket, c_addr = self.listener.accept()           # get socket and client address from listener
        client = AggClient(c_socket, c_addr, self.next_id)  # create aggclient instance which stores socket and metadata
        self.clients.append(client)
        self.next_id += 1
        log(f'[{client.id}] Connected new client {c_addr}')

    def recv_all_weights(self):
        for client in self.clients:
            data = self.recv(client)
            client.weights = int.from_bytes(data, 'big')

    def send_all_weights(self):  # now also with ipfs
        for client in self.clients:
            client.socket.sendall(self.hash.encode('utf-8'))
            client.socket.sendall(self.aggregated_weights.to_bytes(1, 'big'))
        self.aggregated_weights = None

    def aggregate(self):
        """
        Aggregation that takes place when weights of all clients are received. Aggregates them and sends them to
        every Client.
        """
        summed_weights = 0
        for client in self.clients:
            summed_weights += client.weights
            client.weights = 0
        self.aggregated_weights = int(summed_weights / len(self.clients))
        log(f"Aggregated Weights: {self.aggregated_weights}")
        # add weights to ipfs
        if os.path.exists('weights.txt'):
            os.remove('weights.txt')
        f = open('weights.txt', 'wb')
        f.write(self.aggregated_weights.to_bytes(1, 'big'))
        f.close()
        log("Start Upload")
        self.hash = self.ipfs_client.add('weights.txt')['Hash']
        log(f"Weights Uploaded with Hash {self.hash}")

    @staticmethod
    def recv(client):
        """
        Takes one client, receives a message containing his current weights and return them
        :param client: Client object which contains his corresponding socket
        :return: Data that was transmitted
        """
        # receive header
        header = client.socket.recv(HEADER_LEN)
        if len(header) != HEADER_LEN:
            raise Exception("Missing Header (in one recv)")
        data_len = int.from_bytes(header, "big")
        data = bytearray()
        total_recvd = 0
        # receive data from client
        while total_recvd < data_len:
            packet = client.socket.recv(data_len - total_recvd)
            if not packet:
                Exception("Missing Data")
            data.extend(packet)
            total_recvd += len(packet)
            log(f"[{client.id}] Received: {int.from_bytes(data, 'big')}")
        return data


if __name__ == '__main__':
    server = Server()
    server.start()
