# Status Codes

STATUS_CODE = {100 : '100 : Wainting',
               200 : '200 : OK',
               400 : '400 Error : Server is full',
               500 : '500 Error : Server problem'}

#Server Datas

HOST = '127.0.0.1'
PORT = 8080

#Client Datas

CLIENT_COUNT = 3

#UI options
CHAT_WIDTH = 600
CHAT_HEIGHT = 500

CHAT_TEXT_HEIGHT = 25
CHAT_TEXT_WIDTH = 70

MAIN_WIDTH = 180
MAIN_HEIGHT = 290

HOST_WIDTH = 250
HOST_HEIGHT = 150

CONN_WIDTH = 200
CONN_HEIGHT = 150

BUTTON_WIDTH = 20
BUTTON_HEIGHT = 2

LABEL_WIDTH = 50
LABEL_HEIGHT = 1

FIELD_WIDTH = 20
FIELD_HEIGHT = 1

TEXT_WIDTH = 30
TEXT_HEIGHT = 30

RESIZABLE_WIDTH = True
RESIZABLE_HEIGHT = True

NOT_RESIZABLE_WIDTH = False
NOT_RESIZABLE_HEIGHT = False

ANCHOR_NORTH = 'n'

# Random names part
RANDOM_START_NAME = ['Random', 'Sussy', 'Bad', 'Ugly', 'Glory', 'Dumb', 'Dull']
RANDOM_END_NAME = ['Boy', 'Girl', 'Wizard', 'Hole', 'Warlock', 'Guy', 'NotSoGuy']

# Random number gen part
START_NUM = 1
END_NUM = 100000

# Regular expression patterns
IP_PATTERN = r''

# Browser values
BROWSERS = ['chrome', 'firefox', 'opera', 'safari']
HELP_LINK = 'https://github.com/Sralker731/Chat-Online/wiki'

# CMD Config
EDGE_PROMPT = f'cmd /c python "start msedge {HELP_LINK}"'
WEBBROWSER_PROMPT = f'cmd /c "python -m webbrowser -t "{HELP_LINK}""'
