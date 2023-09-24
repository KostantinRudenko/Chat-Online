import tkinter.messagebox as mb
import os

from tkinter import *
from config import *
from engine import Engine
from chat_window import *

def host_window():
    '''
    Window for creating a new server(chat)
    '''
    def check():
        '''
        Checking if server ip or server port are entered for creating the server
        '''
        global ip, port, is_host
        eng = Engine()
        is_host = True
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
            chat_windows = ChatWindow()
            chat_windows.admin_window(ip, port)

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
    '''
    Window for connecting to a server(chat)
    '''
    def check():
        '''
        Checking if ip and port are entered or one(both) of them isn't(aren't)
        '''
        global client_ip, client_port
        eng = Engine()
        client_ip = ip_field.get(0.0, END).strip()
        client_port = port_field.get(0.0, END).strip()
        check_list = [eng.is_empty(client_ip), eng.is_ip(client_ip), eng.is_port(client_port)]
        check_count = 0
        for check in check_list:
            if not check:
                mb.showerror(title='Error!',
                             message='Error. Something is wrong! Please, check your IP or port!')
                break
            check_count += 1
        if check_count == len(check_list):
            chat_windows = ChatWindow()
            #FIXME needs to write what will happen if client connect
            
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

def close_window():
    Engine.window_destroy(window, False)

window = Tk()
main_engine = Engine()
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

empty_label3 = Label(width=LABEL_WIDTH,
                     height=LABEL_HEIGHT)

help_button = Button(width=BUTTON_WIDTH,
                     height=BUTTON_HEIGHT,
                     text='Help',
                     command=main_engine.open_help_link)

empty_label4 = Label(width=LABEL_WIDTH,
                     height=LABEL_HEIGHT)

close_button = Button(width=BUTTON_WIDTH,
                      height=BUTTON_HEIGHT,
                      text='Exit',
                      command=close_window)

widgets = [option_label, empty_label1, create_button, empty_label2, connect_button, empty_label3,
           help_button, empty_label4, close_button]

for widget in widgets:
    widget.pack(anchor=ANCHOR_NORTH)

window.mainloop()