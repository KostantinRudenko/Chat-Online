from client import *
from server import *
import tkinter.messagebox as mb

import threading
from tkinter import *
from config import *
from engine import Engine

class ChatWindow:

    '''
    Class with two types of chat windows.

    First is the chat window for client to send messages and receive them from other clients.

    Second is the chat window only for receicing the messages which the clients sends.
    
    The first window should opens when the client was connected to the server.
    And the second window should opens when the server was created.
    '''

    def __init__(self) -> None:
        self.eng = Engine()
        self.client = Client()
        self.main_server = None
        self.server_threads = None
        self.client_threads = None
        self.admin_chat_window = None

    def print_message(self, message, chat_field : Text):
        '''
        Print messages into the chat field.
        '''
        if message == None:
            pass
        else:
            chat_field.insert(index='0.0', chars=message)
            try:
                self.eng.write_log(f'[STATUS: RECEIVED MESSAGE] {message.decode()}\n')
            except:
                self.eng.write_log(f'[STATUS: RECEIVED MESSAGE] {message}\n')

    def close_conn(self, subject : 1 | 0,
                   threads : list[threading.Thread] = None,
                   buttons : list[Button] = None):
        '''
        Closes the connection with the subject, close threads, disables buttons
        '''
        if subject == 1:
            self.main_server.close()
            IS_HOST = False

        elif subject == 0:
            self.client.close()
            IS_SOCKET = False

        if threads != None:
            self.eng.thread_destroy(threads)
        
        if buttons != None:
            self.eng.disable_button(buttons)

        del self.server_threads
        del threads
        del self.client_threads
        del subject
        del buttons        
        mb.showinfo(title='Staus',
                    message='The connection is closed!')
    
    def broadcasting(self, chat_field : Text):
        '''
        Sends the message to every client and insert it into the admin chat field
        '''
        data = self.main_server.broadcast_message()
        for false_data in [None, '']:
            if data == false_data:
                pass
        else:
            self.print_message(data, chat_field)

    def chat_window(self, ip, port):
        '''
        Opens simple chat window for client.
        Client is able to send messages via this window.
        '''
        username = self.eng.generate_random_name()
        mb.showinfo(title='Your name!',
                    message=f'Your name is {username}. Welcome to the chat!')
        self.client.connect_to(ip, port)

        def send_message(message_field):
            '''
            Sends messages to server. 
            '''
            message = message_field.get(0.0, END)
            message_field.delete(0.0, END)
            
            self.client.send_message(f'{self.eng.current_time()} {username} {message}')
            chat_field.insert(0.0, f'{self.eng.current_time()} {username} {message}')
            self.eng.write_log(f'[STATUS: SEND MESSAGE] {self.eng.current_time()} {message}')
        
        def receiving(chat_field : Text):
            '''
            Receives messages from server and print them into the chat field
            '''
            data = self.client.receive_message()
            if data is list:
                self.close_conn(subject=0,
                                threads=self.client_threads,
                                buttons=[send_button, close_button])
            else:
                self.print_message(data, chat_field)

        alt_window = Toplevel()
        alt_window.geometry(f'{CLIENT_CHAT_WIDTH}x{CLIENT_CHAT_HEIGHT}')
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
                            command=lambda: send_message(message_field))
        
        empty_lable = Label(alt_window,
                    width=LABEL_WIDTH,
                    height=LABEL_HEIGHT)

        close_button = Button(alt_window,
                    width=BUTTON_WIDTH,
                    height=BUTTON_HEIGHT,
                    text='Exit!',
                    command=lambda: self.close_conn(0, self.client_threads, 
                                                    [send_button, close_button]))

        widgets = {chat_label : (0, 3),
                chat_field : (1, 3),
                scrollbar : (1, 4),
                message_label : (2, 3),
                message_field : (3, 3),
                send_button : (4, 3),
                empty_lable : (5, 3),
                close_button : (6, 3)}
        chat_field['yscrollcommand'] = scrollbar.set
        for widget, coords in widgets.items():
            row_pos, col = coords
            widget.grid(row=row_pos,
                        column=col)
        
        def thread_receiving():
            while True:
                receiving(chat_field)

        postman = threading.Thread(target=thread_receiving)

        self.client_threads = [postman]

        postman.start()

    def admin_window(self, ip, port):
        '''
        Opens server chat window.
        It should be used by admin(server) for checking or watching the correspondence of the clients.
        '''

        alt_window = Toplevel()
        alt_window.geometry(f'{CHAT_WIDTH}x{CHAT_HEIGHT}')
        alt_window.resizable(NOT_RESIZABLE_WIDTH, NOT_RESIZABLE_HEIGHT)
        alt_window.title('Chat window (ADMIN MODE)')
        
        chat_label = Label(alt_window,
                        width=LABEL_WIDTH,
                        height=LABEL_HEIGHT,
                        text='Chat window')
        
        self.admin_chat_window = Text(alt_window,
                        width=LOG_CHAT_WIDTH,
                        height=LOG_CHAT_HEIGHT)
        
        scrollbar = Scrollbar(alt_window,
                            orient=VERTICAL,
                            command=self.admin_chat_window.yview)
        
        close_button = Button(alt_window,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
            text='Close the Server',
            command=lambda: self.close_conn(subject=1,
                                            threads=self.server_threads,
                                            buttons = [close_button])
                            )
        widgets = {chat_label : (0, 3),
       self.admin_chat_window : (1, 3),
                    scrollbar : (1, 4),
                 close_button : (2, 3)}
        
        self.admin_chat_window['yscrollcommand'] = scrollbar.set
        for widget, coords in widgets.items():
            row_pos, col = coords
            widget.grid(row=row_pos,
                        column=col)
        
        self.main_server = Server(ip, int(port))

        def accepting():
            '''
            Accepts clients, trying to connect to the chat
            '''
            while True:
                self.main_server.client_accepting()

        def receiv():
            while True:
                self.broadcasting(self.admin_chat_window)

        '''
        # The thread writes and sends messages
        writer = threading.Thread(target=broadcasting, name='Message Writer')
        '''
        # This thread accepts the clients
        guard = threading.Thread(target=accepting, name="Servant of the People")
        receiver = threading.Thread(target=receiv)
        self.server_threads = [receiver, guard]
        guard.start()
        receiver.start()