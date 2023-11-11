class Error400(Exception):
    '''
    400 : Socket is not able to connect to the server
    '''
    pass
class Error500(Exception):
    '''
    500 : Server problem(ooops...)
    '''
    pass