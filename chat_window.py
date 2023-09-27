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
        self.threads = None

    def print_message(self, message, chat_field):
        '''
        Print messages into the chat field.
        '''
        chat_field.insert(0.0, message)
        self.eng.write_log(f'[STATUS: RECEIVED MESSAGE] {message}')
    
    def close_conn(self):
        '''
        Closes the server
        '''
        self.main_server.close()
        self.eng.thread_destroy(self.threads)
        self.close_button.config(state='disabled')
        mb.showinfo(title='Server Staus',
                    message='The server is closed!')

    def chat_window(self, ip, port):
        '''
        Opens simple chat window for client.
        Client is able to send messages via this window.
        '''
        username = self.eng.generate_random_name()
        mb.showinfo(title='Your name!',
                    message=f'Your name is {username}. Welcome to the chat!')
        self.client.connect_to(ip, port)

        def send_message():
            '''
            Sends messages to server. 
            '''
            message = message_field.get(0.0, END)
            message_field.delete(0.0, END)
            
            self.client.send_message(f'{self.eng.current_time()} {username} {message}')
            chat_field.insert(0.0, f'{self.eng.current_time()} {username} {message}' + '\n')
            
            self.eng.write_log(f'[STATUS: SEND MESSAGE] {message}')
        
        def close_connection(client : socket.socket, buttons : list[Button]):
            client.close()
            self.main_server.send(CLOSE_MESSAGE)
            for button in buttons:
                button.config(default='disabled')
    
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
                            command=send_message)
        
        empty_lable = Label(alt_window,
                    width=LABEL_WIDTH,
                    height=LABEL_HEIGHT)

        close_button = Button(alt_window,
                      width=BUTTON_WIDTH,
                      height=BUTTON_HEIGHT,
                      text='Exit!',
                      command=lambda: close_connection(self.client, [send_button, close_button]))
        
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
        
        self.close_button = Button(alt_window,
                              height=BUTTON_HEIGHT,
                              width=BUTTON_WIDTH,
                              text='Close the Server',
                              command=self.close_conn)

        widgets = {chat_label : (0, 3),
                   chat_field : (1, 3),
                    scrollbar : (1, 4),
                 self.close_button : (2, 3)}
        
        chat_field['yscrollcommand'] = scrollbar.set
        for widget, coords in widgets.items():
            row_pos, col = coords
            widget.grid(row=row_pos,
                        column=col)
        
        server = Server(ip, port)
        self.main_server = server.create_server()

        def accepting():
            '''
            Accepts clients, trying to connect to the chat
            '''
            while True:
                server.client_accepting()
        
        def broadcasting():
            '''
            Sends the message to every client and insert it into the admin chat field
            '''
            data = server.broadcast_message(server.clients)
            try:
                if int(data) == 1:
                    pass
            except:
                pass
            self.print_message(data, chat_field)

        def close_connect():
            '''
            er...
            '''
            for found in range(len(server.clients)): # FIXME - Bad realization. Need to improve code
                if server.clients[found] == self.client:
                    server.clients.pop(found)
            del self.client

        # The thread writes and sends messages
        writer = threading.Thread(target=broadcasting, name='Message Writer')
        # This thread accepts the clients
        guard = threading.Thread(target=accepting, name="Servant of the People")
        
        self.threads = [writer, guard]

        guard.start()
        writer.start()