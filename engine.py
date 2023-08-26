import re

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