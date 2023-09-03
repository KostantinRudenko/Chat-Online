'''
400 : Socket is not able to connect to the server
401 : Socket trying ot connect to the full server
500 : Unknown server problem
501 : Server is not able to accept the socket connecting
502 : Server has turned off of crowded
'''
class Error400(Exception):
    pass

class Error401(Exception):
    pass

class Error500(Exception):
    pass

class Error501(Exception):
    pass

class Error502(Exception):
    pass