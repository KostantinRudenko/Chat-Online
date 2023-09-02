from tkinter import *
from config import *

from engine import Engine

import tkinter.messagebox as mb

def chat_window():
    def send_message():
        nonlocal username
        message = message_field.get(0.0, END)
        message_field.delete(0.0, END)
        chat_field.insert(0.0, f'{eng.current_time()} {username} {message}')
    eng = Engine()
    username = eng.generate_random_name()
    mb.showinfo(title='Your name!',
                message=f'Your name is {username}. Welcome to the chat!')
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
    