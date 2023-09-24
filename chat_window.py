from client import *
from server import *
import tkinter.messagebox as mb

import threading
from tkinter import *
from config import *
from main import window
from engine import Engine

class ChatWindow:

    '''
    Class with two types ofchat windows.

    First is the chat window for client to send messages and receive them from other clients.

    Second is the chat window only for receicing the messages which the clients sends.
    
    The first window should opens when the client was connected to the server.
    And the second window should opens when the server was created.
    '''

    def __init__(self) -> None:
        self.eng = Engine()
        self.clients = {}

    def print_message(self, message, chat_field):
        '''
        Print messages into the chat field.
        '''
        chat_field.insert(0.0, message)
        self.eng.write_log(f'[STATUS: RECEIVED MESSAGE] {message}')

    def chat_window(self, ip, port):
        '''
        Opens usuall chat window for client.
        Client is able to send messages via this window.
        '''
        username = self.eng.generate_random_name()
        mb.showinfo(title='Your name!',
                    message=f'Your name is {username}. Welcome to the chat!')
        
        client = Client()
        client.connect_to(ip, port)

        def send_message():
            '''
            Sends messages to server. 
            '''
            message = message_field.get(0.0, END)
            message_field.delete(0.0, END)
            
            client.send_message(f'{self.eng.current_time()} {username} {message}')
            chat_field.insert(0.0, f'{self.eng.current_time()} {username} {message}' + '\n')
            
            self.eng.write_log(f'[STATUS: SEND MESSAGE] {message}')
    
        alt_window = Toplevel()
        alt_window.geometry(f'{CHAT_WIDTH}x{CHAT_HEIGHT}')
        alt_window.resizable(NOT_RESIZABLE_WIDTH, NOT_RESIZABLE_HEIGHT)
        alt_window.title('Chat window')
        chat_label = Label(alt_window,
                        width=LABEL_WIDTH,
                        height=LABEL_HEIGHT,
                        text='Chat window')
        chat_field = Text(alt_window,
                        width=CHAT_TEXT_WIDTH,
                        height=CHAT_TEXT_HEIGHT)
        
        scrollbar = Scrollbar(alt_window,
                            orient=VERTICAL,
                            command=chat_field.yview)
        message_label = Label(alt_window,
                            width=LABEL_WIDTH,
                            height = LABEL_HEIGHT,
                            text='Enter your message below')
        
        message_field = Text(alt_window,
                            width=FIELD_WIDTH,
                            height=FIELD_HEIGHT)
        
        send_button = Button(alt_window,
                            width=BUTTON_WIDTH,
                            height=BUTTON_HEIGHT,
                            text='SEND!',
                            command=send_message)
        
        widgets = {chat_label : (0, 3),
                chat_field : (1, 3),
                scrollbar : (1, 4),
                message_label : (2, 3),
                message_field : (3, 3),
                send_button : (4, 3)}
        chat_field['yscrollcommand'] = scrollbar.set
        for widget, coords in widgets.items():
            row_pos, col = coords
            widget.grid(row=row_pos,
                        column=col)

    def admin_window(self, ip, port):
        '''
        Opens server chat window.
        It should be used by admin(server) for checking or watching the correspondence of the clients.
        '''

        alt_window = Toplevel()
        alt_window.geometry(f'{CHAT_WIDTH}x{CHAT_HEIGHT}')
        alt_window.resizable(NOT_RESIZABLE_WIDTH, NOT_RESIZABLE_HEIGHT)
        alt_window.title('Chat window')
        
        chat_label = Label(alt_window,
                        width=LABEL_WIDTH,
                        height=LABEL_HEIGHT,
                        text='Chat window')
        
        chat_field = Text(alt_window,
                        width=CHAT_TEXT_WIDTH,
                        height=CHAT_TEXT_HEIGHT)
        
        scrollbar = Scrollbar(alt_window,
                            orient=VERTICAL,
                            command=chat_field.yview)

        widgets = {chat_label : (0, 3),
                   chat_field : (1, 3),
                    scrollbar : (1, 4)}
        
        chat_field['yscrollcommand'] = scrollbar.set
        for widget, coords in widgets.items():
            row_pos, col = coords
            widget.grid(row=row_pos,
                        column=col)
        
        server = Server(ip, port)

        def accepting():
            '''
            Accepts clients, trying to connect to the chat
            '''
            while True:
                for client, addr in server.client_accepting():
                    if not client or not addr:
                        pass
                    self.clients[addr] = client
        
        def broadcasting():
            '''
            Sends the message to every client and insert it into the admin chat field
            '''
            data = server.broadcast_message(self.clients)
            self.print_message(data, chat_field)

        # The thread writes and sends messages
        writer = threading.Thread(target=broadcasting, name='Message Writer')
        # This thread accepts the clients
        guard = threading.Thread(target=accepting, name="Servant of the People")
        # This thread "kills" the threads and close the application
        closer = threading.Thread(target=self.eng.is_open(),
                                  name='John Wick', args=(window, True, [writer, guard, closer]))

        guard.start()
        writer.start()
        closer.start()