import socket
from config import *
from server import *


class Client:

    def socket_client(massage):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        while True:
            data = client_socket.recv(1024)
            return data