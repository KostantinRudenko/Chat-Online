import socket
from config import *

class Server:
    
    def socket_server(self):
        client_count = 0
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(CLIENT_COUNT)
        print("Server is ready!")
        
        while True:
            if client_count > CLIENT_COUNT:
                server_socket.send(STATUS_CODE[400])
            else:
                client, addr = server_socket.accept()
                client_count += 1
                print(f'{addr} is connected')

if __name__ == "__main__":
    server = Server()
    server.socket_server()
