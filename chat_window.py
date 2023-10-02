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
        self.close_button = None
        self.server_threads = None
        self.client_threads = None

    def print_message(self, message, chat_field : Text):
        '''
        Print messages into the chat field.
        '''
        chat_field.insert(0.0, message)
        self.eng.write_log(f'[STATUS: RECEIVED MESSAGE] {message}')
    
    def close_conn(self, subject : socket.socket,
                   threads : list[threading.Thread] = None,
                   buttons : list[Button] = None,
                   is_client : bool = False,
                   chat : Text = None):
        '''
        Closes the connection with the subject, close threads, disables buttons
        '''
        if is_client:
            subject.send(CLOSE_MESSAGE)
        
        chat.insert(0.0, 'Connection is closed!')
        subject.close()

        if threads != None:
            self.eng.thread_destroy(threads)
            if not is_client:
                del self.server_threads
                del threads
            else:
                del self.client_threads
        
        if buttons != None:
            self.eng.disable_button(buttons)

        del subject
        
        mb.showinfo(title='Staus',
                    message='The connection is closed!')

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
            
            self.client.send_message(f'{self.eng.current_time()} {username} {message}' + '\n')
            chat_field.insert(0.0, f'{self.eng.current_time()} {username} {message}' + '\n')
            
            self.eng.write_log(f'[STATUS: SEND MESSAGE] {message}')
        
        def receiving(chat_field : Text):
            '''
            Receives messages from server and print them into the chat field
            '''
            data = self.client.receive_message()
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
                    command=lambda: self.close_conn(self.client, self.client_threads, 
                                                    [send_button, close_button], True))

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
        
        postman = threading.Thread(target=receiving, args=chat_field)

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
        
        chat_field = Text(alt_window,
                        width=LOG_CHAT_WIDTH,
                        height=LOG_CHAT_HEIGHT)
        
        scrollbar = Scrollbar(alt_window,
                            orient=VERTICAL,
                            command=chat_field.yview)
        
        close_button = Button(alt_window,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
            text='Close the Server',
            command=lambda:
            
            self.close_conn(subject=self.main_server.server_socket,
                                            threads=self.server_threads,
                                            buttons = [close_button],
                                            chat=chat_field)
                              )
        widgets = {chat_label : (0, 3),
                   chat_field : (1, 3),
                    scrollbar : (1, 4),
                    close_button : (2, 3)}
        
        chat_field['yscrollcommand'] = scrollbar.set
        for widget, coords in widgets.items():
            row_pos, col = coords
            widget.grid(row=row_pos,
                        column=col)
        
        self.main_server = Server(ip, port)

        def accepting():
            '''
            Accepts clients, trying to connect to the chat
            '''
            while True:
                self.main_server.client_accepting()
        
        def broadcasting():
            '''
            Sends the message to every client and insert it into the admin chat field
            '''
            data = self.main_server.broadcast_message(
                                    self.main_server.clients)
            try:
                if int(data) == 0:
                    pass
            except:
                pass
            self.print_message(data, chat_field)

        # The thread writes and sends messages
        writer = threading.Thread(target=broadcasting, name='Message Writer')
        # This thread accepts the clients
        guard = threading.Thread(target=accepting, name="Servant of the People")
        
        self.server_threads = [writer, guard]

        guard.start()
        writer.start()