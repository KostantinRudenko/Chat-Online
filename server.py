import socket
import select
import threading
from functools import partial
from config import *

class Server: # Main class
    def __init__(self) -> None: # This function run the server and save total info
        self.connected_clients = []
        self.connected_clients_addr=[]
        self.client_count = 0

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(CLIENT_COUNT)

        print("Server is ready!")

    def socket_server(self): # This function makes server works
        while True:
            client_socket, addr = self.server_socket.accept()
            self.client_data_saving(client_socket, addr)
            self.broadcast_message(client_socket)
            
            client_thread = threading.Thread(target=partial(self.broadcast_message, client_socket))
            client_thread.start()
            
            if self.client_count > CLIENT_COUNT:
                self.server_socket.send(STATUS_CODE[400])
                break
        
    def broadcast_message(self, client_socket): # This method sends massages to every connected client
        client_thread = threading.Thread(target=self.broadcast_message, args=(client_socket,))
        client_thread.start()
        
        try:
            ready_to_read, _, _ = select.select([client_socket], [], [], 0)
            if ready_to_read:
                data = client_socket.recv(1024)
                if not data:
                    pass

                for client in self.connected_clients:
                    if client != client_socket:
                        client.send(data)
                    else:
                        client.send(b'Massage was sent!')
        except socket.error as e:
            if e.errno == 10035:
                pass

    def client_data_saving(self, client_socket, addr): # This method accepts clients which wants to connect        
        self.client_count += 1
        
        self.connected_clients.append(client_socket)
        self.connected_clients_addr.append(addr)
        
        print(f'{addr} is connected')
        result = client_socket
        return result

if __name__ == "__main__":
    server = Server()
    server.socket_server()