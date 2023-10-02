import re
import os

from datetime import datetime
from tkinter import Tk
from tkinter import Button
from random import *
import threading
from config import *

class Engine:
    def __init__(self) -> None:
        self.event = threading.Event()

    def read_data(self, text : str, regex_option = None) -> str:
        '''
        Function reads a text from UI part
        text - string value 
        regex_option - pattern to search items in the text. None was set as default
        '''
        if regex_option is None:
            return text
        else:
            search_results = re.findall(regex_option, text)
            return search_results
    def generate_random_name(self) -> str:
        '''
        Function generates random name to user and returns user name as a string
        '''
        random_first = choice(RANDOM_START_NAME)
        random_second = choice(RANDOM_END_NAME)
        random_number = str(randint(START_NUM, END_NUM))
        return random_first + random_second + '#' + random_number
    
    def is_empty(self, string : str) -> bool:
        '''
        Check if string is empty. Returns a bool (True\False)
        True - fields are not empty
        False - fields are empty
        '''
        return len(string) != 0
    
    def is_port(self, string : str) -> bool:
        '''
        Check if port is numeric. Returns a bool (True\False)
        True - fields are numeric
        False - fields are not numeric
        '''
        return string.isnumeric() and len(string) <= 5

    def is_ip(self, string : str) -> bool:
        '''
        Check if string contains IP. Returns a bool (True\False)
        True - IP is correct
        False - IP is not correct
        '''
        ip_numbers = string.split('.')
        if len(ip_numbers) > 4:
            return False
        count = 0
        for value in ip_numbers:
            if value.isnumeric() and len(value) <= 3:
                count += 1
        return count == 4
    def current_time(self) -> str:
        '''
        returns a time in the string format
        Example: 10:00:00
        '''
        time = datetime.now()
        return f'[{time.hour}:{time.minute}:{time.second}]'
    
    def write_log(self, string) -> str:
        '''
        sends all data to the log file
        '''
        log_file = open('log.txt', 'a')
        date = datetime.now()
        today = f'DATE FOR THE {date.year}-{date.month}-{date.day}'
        
        with open('log.txt', 'r') as file:
            text = file.read()
            data = self.read_data(text, r'DATA FOR THE \d+-\d+-\d+')
            
            if data[-1] == today:
                log_file.write(string)
            log_file.write(today + '\n' + string + '\n')
            
            file.close()
        log_file.close()
    
    def window_destroy(window : Tk):
        '''
        Destroys window
        '''
        window.destroy()
    
    def thread_destroy(self, threads : list[threading.Thread]):
        '''
        Closes all of the threads that were given to it as arguments
        '''
        import ctypes
        for thread in threads:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), 
                                                           ctypes.py_object(SystemExit))
    
    def disable_button(self, buttons : list[Button]):
        '''
        makes the buttons disabled
        '''
        for button in buttons:
            button.config(state='disabled')

    def open_help_link(self):
        '''
        Open Link to the WIKI page
        '''
        try:
            os.system(WEBBROWSER_PROMPT)
        except:
            os.system(EDGE_PROMPT)
