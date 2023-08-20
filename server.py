import socket
from config import *

class Server:
    
    def chat():
        client_count = 0
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(CLIENT_COUNT)

        while True:
            client = server_socket.accept()
            client_count += 1
            client.send(f'{client} connected'.encode())
            if client_count > CLIENT_COUNT:
                return STATUS_CODE[400]