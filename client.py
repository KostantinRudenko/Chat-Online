import socket
from config import *


class Client:

    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((HOST, PORT))
        print('You are connected')


    def socket_client(self):
        while True:
            massage = input("Massage: ")
            self.server_socket.send(massage.encode())
            data = self.server_socket.recv(1024).decode()
            if not data:
                continue
            
            elif data:
                print(data)

if __name__ == "__main__":
    client = Client()
    client.socket_client()
