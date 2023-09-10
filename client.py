import socket
import threading
from config import *


class Client:

    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((HOST, PORT))

    def receive_message(self):
        '''
        Receives messages from server and return them.
        '''
        while True:
            data = self.server_socket.recv(1024).decode()
            yield data
    
    def send_message(message : str, self):
        '''
        Sends message to server.
        '''
        while True:
            self.server_socket.send(message.encode())

if __name__ == "__main__":
    client = Client()

    send_thread = threading.Thread(target=client.send_message, daemon=False)
    receive_thread = threading.Thread(target=client.receive_message, daemon=False)
    
    send_thread.start()
    receive_thread.start()