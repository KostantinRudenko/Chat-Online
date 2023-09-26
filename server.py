import socket
import select

from config import *
from exceptions import *

class Server:
    '''
    This class has functions for starting a new server and accepting clients.
    '''

    def __init__(self, host, port) -> None:
        '''
        Runs the server. Saves total info
        '''
        self.client_count = 0
        self.server_socket = None
        self.host = host
        self.port = port
        self.clients = {}
    
    def create_server(self):
        '''
        Creates a new server and returns the socket
        '''
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, int(PORT))) #FIXME set self.host + self.port instead of config values
        self.server_socket.listen(CLIENT_COUNT)

        return self.server_socket
        
    def broadcast_message(self, clients : dict) -> str:
        '''
        Receives messages from clients and sends them to every client.
        '''
        while True:
            for _, client_socket in clients.items():
                ready_to_read, _, _ = select.select([client_socket], [], [], 0)
                if ready_to_read:
                    data = client_socket.recv(1024)
                    if not data:
                        pass
                    else:
                        for client in clients.values():
                            client.send(data)
                        return data

    def client_accepting(self):
        '''
        Accepts inccoming client's connections. Saves clients socket and address.
        
        '''
        client, addr = self.server_socket.accept()

        self.client_count += 1
        self.clients[addr] = client