import socket
from config import *


class Client():
    '''
    Client class has methods for connection to a server, receiving and message sending
    '''
    def __init__(self) -> None:
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to(self, ip : str, port : int) -> None:
        '''
        Connects client to the server(chat)
        '''
        self.client_socket.connect((ip, int(port)))

    def receive_message(self):
        '''
        This function receives messages
        '''
        try:
            data = self.client_socket.recv(1024).decode()
            if data == CLOSE_SERVER_MESSAGE.decode():
                data = []
            return data
        except:
            pass

    def send_message(self, message) -> None:
        '''
        This function sends messages to server
        '''
        self.client_socket.send(message.encode())

    def close(self):
        self.client_socket.send(CLOSE_MESSAGE)
        self.client_socket.close()