import socket
from config import *
from server import *


class Client:

    def socket_client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print('You are connected')
        while True:
            data = client_socket.recv(1024).decode()
            print(data)

if __name__ == "__main__":
    client = Client()
    client.socket_client()
