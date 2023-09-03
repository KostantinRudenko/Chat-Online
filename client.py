import socket
import select
from config import *


class Client:

    def __init__(self, ip, port) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(ip, port)
        print('You are connected')


    def socket_client(self, client_message): # This function sends and recieve messages
        while True:
            self.server_socket.setblocking(0)

            ready = select.select([self.server_socket], [], [], 2)
            if ready[0]:
                result = self.receive_message()
            else:
                self.server_socket.send(client_message.encode())
    
    def recieve_message(self):
        data = self.server_socket.recv(1024).decode()
        return data
    
    def send_message(self, client_message):
        self.server_socket.send(client_message.encode())

if __name__ == "__main__":
    client = Client()
    client.socket_client()
