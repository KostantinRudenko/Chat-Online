'''import socket'''
import select
import asyncio

from config import *
from exceptions import *

class Server(asyncio.Protocol): # Main class
    '''
    This class has functions for starting a new server and accepting clients.
    '''

    async def __init__(self) -> None:
        '''
        Runs the server. Saves total info
        '''
        self.connected_clients = {}
        self.client_count = 0

    def broadcast_message(self):
        '''
        Receives messages from clients and sends them to every client.
        '''
        while True:
            for client_socket in self.connected_clients:
                ready_to_read, _, _ = select.select([client_socket], [], [], 0)
                if ready_to_read:
                    data = client_socket.recv(1024)
                    if not data:
                        pass
                    else:
                        for client in self.connected_clients:
                            if client == client_socket:
                                client.send(b'200 : OK')
                            elif client != client_socket:
                                client_socket.send(data)

    def client_accepting(self, transport) -> None:
        '''
        Accepts inccoming client's connections. Saves clients socket and address.
        
        '''
        client = transport.get_exctra_info('peername')
        self.connected_clients[id(client)] = client
        while True:
            pass

async def main():
    server = await asyncio.start_server(Server, HOST, PORT)
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())