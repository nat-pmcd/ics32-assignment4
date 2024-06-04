# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

"""
Contains the DirectMessenger class, to manage sending
and receiving data with the dsu server.
"""

import socket
from time import time
import ds_protocol as dsp
PORT = 6000
SERVER = "localhost"


class DirectMessage:
    """
    temp docstring
    """


class DirectMessenger:
    """
    Manages server connection, authentication, and sending/receiving messages.
    Requires server (string) and port (int)
    
    Parameters
    --------
    server : str
        IP address the client should attempt to connect to
    port : int
        The port of the IP address the client connects to
    """
    def __init__(self, server: str = SERVER, port: int = PORT) -> None:
        self.server = server
        self.port = port
        self.token = None
        self.socket = None

    def _connect_to_server(self) -> bool:
        """
        Attempts to establish a socket connection using current server/port
        values. Creates socket attribute and returns if successful.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            address = self.server, self.port
            self.socket.connect(address)
            return True
        except (OSError, TimeoutError) as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            self.socket = None
            return False

    def _send_command(self, command: str) -> dsp.Response:
        """
        Attempts to connect to a server and send json string `command` if
        successful. Returns the response sent by the server.

        Parameters
        --------
        command : str
            json command to send to the server.
        """
        self._connect_to_server()
        if not self.socket:
            print("Could not connect to server.")
            return None

        conn = dsp.init(self.socket)
        resp = dsp.send_command(conn, command)
        print("Sent", command, "and received", resp)
        dsp.close_conn(conn)

        if resp.type == "error":
            print(f"Error occured when sending command! {resp.message}")

        return resp

    def _verify_nonblank(self, content: str, target: str = "string") -> bool:
        """
        Given a string, checks if string is nonblank and not pure whitespace.
        If string is plublishable, returns True.

        Parameters
        --------
        content : str
            The string to verify
        target : str
            If string fails, prints no valid target.
        """
        if isinstance(content, str) and not content.isspace() and content:
            return True
        print(f"No {target} bio to send.")
        return False

    def login(self, username: str, password: str) -> bool:
        """
        Sends the login command to the server, to set token attribute for
        authentication. Returns if successful or not. If not connected to 
        server, attempts to connect first.

        Parameters
        --------
        username : str
            The `username` of the account we're logging into
        password : str
            The `password` of the account we're logging into
        """
        if not self.socket and not self._connect_to_server():
            return False

        join_command = (r'{"join": {"username": "' +
                        username +
                        r'","password": "' +
                        password +
                        r'","token":""}}')

        response = self._send_command(join_command)

        if response.type != "error":
            self.token = response.token
            return True
        return False

    def update_bio(self, bio: str) -> bool:
        """
        Sends the bio command to the server. Returns if successful or not.

        Parameters
        --------
        bio : str
            The text to update the bio into.
        """
        if not self._verify_nonblank(bio):
            return False

        bio_command = (r'{"token":"' +
                       self.token +
                       r'", "bio": {"entry": "' +
                       bio +
                       r'","timestamp": "' +
                       str(time()) + r'"}}')
        response = self._send_command(bio_command)

        return response.type != "error"

    def publish_post(self, msg: str) -> bool:
        """
        Sends the publish command to the server. Returns if successful or not.

        Parameters
        --------
        msg : str
            The text we wish to publish as a post to the server.
        """
        if not self._verify_nonblank(msg):
            return False

        publish_command = (r'{"token":"' +
                           self.token +
                           r'", "post": {"entry": "' +
                           msg +
                           r'","timestamp": "' +
                           str(time()) +
                           r'"}}')
        response = self._send_command(publish_command)

        return response.type != "error"

    def _get_dms(self, only_new: bool = False) -> list[DirectMessage]:
        """
        Gets directmessages from connected server and returns list.
        
        Parameters
        --------
        only_new : bool
            If True, returns only new messages.
        """
        raise NotImplementedError

    def send(self, message: str, recipient: str) -> bool:
        """
        Sends the directmessage command to the server.
        Returns if successful or not.
        
        Parameters
        --------
        message : str
            The `message` we intend on sending to `recipient`.
        recipient : str
            The `recipient` who we intend on sending `message` to.
        """
        if not self._verify_nonblank(message):
            return False
        if not self._verify_nonblank(recipient):
            return False

        dm_command = (r'{"token":"' +
                           self.token +
                           r'", "directmessage": {"entry": "' +
                           message +
                           r'","recipient": "' +
                           recipient +
                           r'","timestamp": "' +
                           str(time()) +
                           r'"}}')
        response = self._send_command(dm_command)

        return response.type != "error"

    def retrieve_new(self) -> list[DirectMessage]:
        """
        Wrapper for _get_dms. Gets all new dms from server and returns
        a list of DirectMessages
        """
        return self._get_dms(only_new=True)

    def retrieve_all(self) -> list[DirectMessage]:
        """
        Wrapper for _get_dms. Gets all new dms from server and returns
        a list of DirectMessages
        """
        return self._get_dms()
