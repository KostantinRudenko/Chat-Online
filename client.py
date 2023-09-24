import socket
import threading
from config import *


class Client():

    def __init__(self) -> None:
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to(self, ip, port):
        '''
        Connects client to the server(chat)
        '''
        self.client_socket.connect((ip, port))

    def receive_message(self):
        '''
        This function receives messages
        '''
        data = self.client_socket.recv(1024).decode()
        return data
    
    def send_message(self, message) -> None:
        '''
        This function sends messages to server
        '''
        self.client_socket.send(message.encode())
