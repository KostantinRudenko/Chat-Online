import socket
import threading
import asyncio
from config import *


class Client(asyncio.Protocol):

    def __init__(self) -> None:
        '''
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((HOST, PORT))
        '''
        self.reader, self.writer = asyncio.open_connection(HOST, PORT)

    async def receive_message(self):
        '''
        Receives messages from server and return them.
        '''
        try:
            while True:
                data = await self.reader.read(100)
                if not data:
                    pass
                else:
                    data.decode()
                    for word in str(data).split():
                        yield word

        except asyncio.CancelledError:
            pass

    async def send_message(self):
        '''
        Sends message to server.
        '''
        while True:
            text = await self.reader.read(100).decode()
            async for word in text.split():
                yield word

if __name__ == "__main__":
    client = Client()

    send_thread = threading.Thread(target=client.send_message, daemon=False)
    receive_thread = threading.Thread(target=client.receive_message, daemon=False)
    
    send_thread.start()
    receive_thread.start()