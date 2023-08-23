import socket
from config import *

class Server:
    def __init__(self) -> None:
        self.connected_clients = []
        self.connected_clients_addr=[]
        self.client_count = 0

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(CLIENT_COUNT)
        print("Server is ready!")
        self.server_socket.send

    def socket_server(self):
        
        while True:
            client_data = self.client_connect()
            client_socket = client_data[0]
            while len(self.connected_clients) != 0:
                data = client_socket.recv(1024)
                self.broadcast_message(client_socket, data)

            if self.client_count > CLIENT_COUNT:
                self.server_socket.send(STATUS_CODE[400])
                break
        
    def broadcast_message(self, client_socket, massage):
        for client_addr in self.connected_clients_addr:
            client_socket.sendto(massage, tuple(client_addr))
    
    def client_connect(self):
        client_socket, addr = self.server_socket.accept()
        self.client_count += 1
        self.connected_clients.append(client_socket)
        self.connected_clients_addr.append(addr)
        print(f'{addr} is connected')
        result = [client_socket, addr]
        return result

if __name__ == "__main__":
    server = Server()
    server.socket_server()
