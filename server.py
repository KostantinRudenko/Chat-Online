import socket
import select
import threading

from config import *
from exceptions import *

class Server: # Main class
    def __init__(self, host, port) -> None:
        '''
        Runs the server. Saves total info
        '''
        self.connected_clients = []
        self.connected_clients_addr=[]
        self.client_count = 0

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(CLIENT_COUNT)

        print("Server is ready!")
        
    def broadcast_message(self):
        '''
        Receives messages from clients and sends them to every client.
        '''
        while True:
            try:
                for client_socket in self.connected_clients:
                    ready_to_read, _, _ = select.select([client_socket], [], [], 0)
                    if ready_to_read:
                        data = client_socket.recv(1024)
                        if not data:
                            pass
                        else:
                            for client in self.connected_clients:
                                if client == client_socket:
                                    client.send(b'200 : OK')
                                elif client != client_socket:
                                    client_socket.send(data)
            except socket.error as e:
                if e.errno == 10035:
                    pass

    def client_accepting(self) -> None:
        '''
        Accepts inccoming client's connections. Saves clients socket and address.
        
        '''
        while True:
            client_socket, addr = self.server_socket.accept()
            client_socket.send(b'You are connected')

            self.client_count += 1
            
            self.connected_clients.append(client_socket)
            self.connected_clients_addr.append(addr)
            
            print(f'{addr} is connected')

if __name__ == "__main__":
    server = Server(HOST, PORT)
    accept_thread = threading.Thread(target=server.client_accepting, daemon=False)
    broadcast_thread = threading.Thread(name='Sanya', target=server.broadcast_message, daemon=False)
        
    accept_thread.start()
    broadcast_thread.start()