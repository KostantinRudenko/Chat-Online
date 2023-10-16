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
        self.client_count = 0 # Count of the connected clients
        self.host = host
        self.port = port
        self.clients = {} # Addresses and sockets of the clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port)) 
        self.server_socket.listen(CLIENT_COUNT)
        
    def broadcast_message(self, clients : dict) -> str | tuple:
        '''
        Receives messages from clients and sends them to every client.
        '''
        try:
            for addr, client_socket in clients.items():
                if not addr:
                    pass
                ready_to_read, _, _ = select.select([client_socket], [], [], 0) # Chaecking if client has sent message
                if ready_to_read:
                    data = client_socket.recv(1024) # Receiving message from the client
                    if not data:
                        pass
                    elif data == CLOSE_MESSAGE:
                        self.clients.pop(addr) # Deleting the client
                        self.client_count -= 1
                        return False
                    else:
                        for client in clients.values():
                            if client != client_socket:
                                client.send(data)
                    return data
        except:
            pass

    def client_accepting(self):
        '''
        Accepts inccoming client's connections. Saves clients socket and address.
        
        '''
        try:
            client, addr = self.server_socket.accept() # Accepting the clients

            self.client_count += 1
            self.clients[addr] = client # Adding the client's address and socket to the dictionary
        except OSError:
            pass

    def close(self):
        '''
        closes the server
        '''
        self.server_socket.close()