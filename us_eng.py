# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

'''
Localization for GUI in English
'''


class DsuEnglish:
    '''
    Contains all English text inside the DSU Manager window.
    '''
    WINDOW_MAIN = 'ICS 32 DS Client'

    TITLE_PROFILE = 'Username'
    HEADER_ACCESS_PROFILE = 'Profile'
    HEADER_DELETE_PROFILE = 'Delete'
    HEADER_MESSAGES_PROFILE = 'Chats'
    BUTTON_ADMIN = 'Toggle Debug'

    BUTTON_CREATE_PROFILE = 'Create Profile'
    BUTTON_ACCESS_PROFILE = 'Profile'
    BUTTON_MESSAGES_PROFILE = 'Chats'
    BUTTON_DELETE_PROFILE = 'Delete'


class ProfileEnglish:
    '''
    Contains all English text inside the DSU Profile window.
    '''
    WINDOW_PROFILE = 'ICS 32 DS Client Profile Manager'

    LABEL_NAME = 'Username: '
    LABEL_PW = 'Password: '
    LABEL_BIO = 'Bio: '

    HEADER_POST = 'Post'
    HEADER_TIME = 'Timestamp'
    HEADER_EDIT = 'Edit'
    HEADER_PUBLISH = 'Publish'
    HEADER_DELETE = 'Delete'

    BUTTON_EDIT_LOGIN = 'Modify Login'

    BUTTON_EDIT_BIO = 'Edit bio'
    BUTTON_PUBLISH_BIO = 'Publish bio'
    BUTTON_PUBLISH_BIO_UNJOINED = 'Join server'

    BUTTON_CREATE_POST = 'Create Post'
    BUTTON_EDIT_POST = 'Edit'
    BUTTON_PUBLISH_POST = 'Publish'
    BUTTON_DELETE_POST = 'Delete'


class MsgEnglish:
    '''
    Contains all English text inside the DSU Messenger window.
    '''
    WINDOW_MSG = 'ICS 32 DS Messenger'

    HEADER_FRIENDS = 'Your Friends'
    HEADER_CHATBOX = 'Chat'

    BUTTON_ADD_FRIEND = 'Add Friend'
    BUTTON_SEND_MSG = 'Send'
    EDITOR_PROMPT_MSG = 'Type a message...'

    STATUS_OK = 'Connected to server'
    STATUS_BAD = 'Connection failed, retrying...'
    STATUS_LOG = 'Error when logging in! Incorrect credentials?'
    LABEL_START = 'To get started, select a friend on the left.'
    LABEL_FRIEND = 'Or add a new friend down below!'


class PromptsEnglish:
    '''
    Contains all English text inside any prompt generated.
    '''
    # CREATE PROFILE
    POPUP_HEADER_CREATE_PROFILE = 'Create a profile'
    POPUP_PROMPT_GET_NAME = 'Enter a username'
    POPUP_PROMPT_GET_NAME_BLANK = 'Username cannot be empty'
    POPUP_PROMPT_GET_NAME_DUPLICATE = "Username already used"
    POPUP_PROMPT_GET_PW = 'Enter a password'
    POPUP_PROMPT_GET_PW_BLANK = 'Password cannot be empty'

    # BIO
    POPUP_HEADER_EDIT_BIO = 'Edit bio'
    POPUP_PROMPT_GET_BIO = 'Describe yourself here!'
    POPUP_PROMPT_GET_BIO_BLANK = 'Bio cannot be empty!'

    # GET SERVER
    POPUP_HEADER_SERVER = 'Select server'
    POPUP_PROMPT_GET_IP = 'Enter the server IP address. Default '
    POPUP_PROMPT_GET_IP_BLANK = 'IP address cannot be blank!'
    POPUP_PROMPT_GET_PORT = 'Enter the server port. Default '
    POPUP_PROMPT_GET_PORT_BLANK = 'Port cannot be blank!'

    POPUP_HEADER_CREATE_POST = 'Create a post'
    POPUP_PROMPT_GET_CONTENT = 'Write your thoughts here!'
    POPUP_PROMPT_GET_CONTENT_BLANK = 'Cannot make an empty post!'

    # EDIT POST
    POPUP_HEADER_EDIT_POST = 'Edit this post'
    POPUP_PROMPT_GET_EDIT = 'Previous post:\n'
    POPUP_PROMPT_GET_EDIT_BLANK = POPUP_PROMPT_GET_CONTENT_BLANK

    # ADD FRIEND
    POPUP_HEADER_ADD_FRIEND = 'Add a friend!'
    POPUP_PROMPT_GET_FRIEND = 'Enter friend name.'
    POPUP_PROMPT_GET_FRIEND_BLANK = "You can't be friends with nobody!"
    POPUP_PROMPT_GET_FRIEND_SELF = "Why are you trying to talk to yourself?"
