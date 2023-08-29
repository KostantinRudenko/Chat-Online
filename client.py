import socket
import select
from config import *


class Client:

    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((HOST, PORT))
        print('You are connected')


    def socket_client(self): # This function sends and recieve messages
        while True:
            self.server_socket.setblocking(0)

            ready = select.select([self.server_socket], [], [], 2)
            if ready[0]:
                data = self.server_socket.recv(1024).decode()
                print(data)
            else:
                massage = input("Massage: ")
                self.server_socket.send(massage.encode())

if __name__ == "__main__":
    client = Client()
    client.socket_client()
