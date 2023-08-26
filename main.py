from tkinter import *

from config import *
from client import Client
from server import Server
from engine import Engine

def host_window():
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
                         text='Create Host!')
    
    widgets = [ip_label, ip_field, port_label, port_field, host_button]

    for widget in widgets:
        widget.pack(anchor=ANCHOR_NORTH)


def connect_window():
    alt_window = Toplevel()
    alt_window.geometry(f'{CONN_WIDTH}x{CONN_HEIGHT}')

    ip_label = Label(alt_window,
                    width=LABEL_WIDTH,
                    height=LABEL_HEIGHT,
                    text = 'Enter IP with port below:')
    
    ip_field = Text(alt_window,
                    width=FIELD_WIDTH,
                    height=FIELD_HEIGHT)
    
    conn_button = Button(alt_window,
                         width=BUTTON_WIDTH,
                         height=BUTTON_HEIGHT,
                         text='Connect!')
    
    widgets = [ip_label, ip_field, conn_button]

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
        
    
        
