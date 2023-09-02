import re

from datetime import datetime
from random import *
from config import *

class Engine:
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
    
