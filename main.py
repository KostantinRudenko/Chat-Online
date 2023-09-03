import tkinter.messagebox as mb

from tkinter import *
from config import *
from engine import Engine
from server import Server
from client import Client

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
    
    if IS_HOST:
        host_server = Server()
    

def host_window():
    def check():
        eng = Engine()
        ip = ip_field.get(0.0, END).strip()
        port = port_field.get(0.0, END).strip()
        check_list = [eng.is_empty(ip), eng.is_ip(ip), eng.is_port(port)]
        check_count = 0
        for check in check_list:
            if not check:
                mb.showerror(title='Error!',
                             message='Error. Something is wrong! Please, check your IP or port!')
                break
            check_count += 1
        if check_count == len(check_list):
            chat_window()

    alt_window = Toplevel()
    alt_window.geometry(f'{HOST_WIDTH}x{HOST_HEIGHT}')

    ip_label = Label(alt_window,
                    width=LABEL_WIDTH,
                    height=LABEL_HEIGHT,
                    text = 'Enter IP below:')
    
    ip_field = Text(alt_window,
                    width=FIELD_WIDTH,
                    height=FIELD_HEIGHT)
    
    port_label = Label(alt_window,
                       width=LABEL_WIDTH,
                       height=LABEL_HEIGHT,
                       text = 'Enter port below:')
    
    port_field = Text(alt_window,
                      width=FIELD_WIDTH,
                      height=FIELD_HEIGHT)
    
    host_button = Button(alt_window,
                         width=BUTTON_WIDTH,
                         height=BUTTON_HEIGHT,
                         text='Create Host!',
                         command=check)
    
    widgets = [ip_label, ip_field, port_label, port_field, host_button]

    for widget in widgets:
        widget.pack(anchor=ANCHOR_NORTH)


def connect_window():
    def check():
        eng = Engine()
        ip = ip_field.get(0.0, END).strip()
        port = port_field.get(0.0, END).strip()
        check_list = [eng.is_empty(ip), eng.is_ip(ip), eng.is_port(port)]
        check_count = 0
        for check in check_list:
            if not check:
                mb.showerror(title='Error!',
                             message='Error. Something is wrong! Please, check your IP or port!')
                break
            check_count += 1
        if check_count == len(check_list):
            chat_window()
    alt_window = Toplevel()
    alt_window.geometry(f'{CONN_WIDTH}x{CONN_HEIGHT}')

    ip_label = Label(alt_window,
                    width=LABEL_WIDTH,
                    height=LABEL_HEIGHT,
                    text = 'Enter IP below:')
    
    ip_field = Text(alt_window,
                    width=FIELD_WIDTH,
                    height=FIELD_HEIGHT)
    
    port_label = Label(alt_window,
                       width=LABEL_WIDTH,
                       height=LABEL_HEIGHT,
                       text = 'Enter port below:')
    
    port_field = Text(alt_window,
                      width=FIELD_WIDTH,
                      height=FIELD_HEIGHT)
    
    conn_button = Button(alt_window,
                         width=BUTTON_WIDTH,
                         height=BUTTON_HEIGHT,
                         text='Connect!',
                         command=check)
    
    widgets = [ip_label, ip_field,
               port_label, port_field, conn_button]

    for widget in widgets:
        widget.pack(anchor=ANCHOR_NORTH)

window = Tk()
window.geometry(f'{MAIN_WIDTH}x{MAIN_HEIGHT}')
window.resizable(NOT_RESIZABLE_WIDTH, NOT_RESIZABLE_HEIGHT)
window.title('Chat Online v1.0.0')

option_label = Label(width=LABEL_WIDTH,
                        height=LABEL_HEIGHT,
                        text="Choose your option")

empty_label1 = Label(width=LABEL_WIDTH,
                    height=LABEL_HEIGHT)

create_button = Button(width=BUTTON_WIDTH,
                        height=BUTTON_HEIGHT,
                        text='Create Chat!',
                        command=host_window)

empty_label2 = Label(width=LABEL_WIDTH,
                    height=LABEL_HEIGHT)

connect_button = Button(width=BUTTON_WIDTH,
                        height=BUTTON_HEIGHT,
                        text = 'Connect to Chat!',
                        command=connect_window)

widgets = [option_label, empty_label1, create_button, empty_label2, connect_button]

for widget in widgets:
    widget.pack(anchor=ANCHOR_NORTH)

window.mainloop()
        
    
        
