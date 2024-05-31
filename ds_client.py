"""

"""
# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

import socket
from time import time
import ds_protocol as dsp
PORT = 6000
SERVER = "localhost"


class Client:
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

    def connect_to_server(self) -> bool:
        """
        Attempts to establish a socket connection using current server/port values.
        Creates socket attribute and returns if successful.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            address = self.server, self.port
            self.socket.connect(address)
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            return False

    def send_command(self, command: str) -> str:
        """
        Attempts to connect to a server and send json string `command` if successful.
        Returns the response sent by the server.

        Parameters
        --------
        command : str
            json command to send to the server.
        """
        self.connect_to_server()
        if not self.socket:
            print("Could not connect to server.")
            return None

        conn = dsp.init(self.socket)
        resp = dsp.send_command(conn, command)
        print("Sent", command, "and received", resp)
        dsp.exit(conn)

        if resp.type == "error":
            print(f"Error occured when sending command! {resp.message}")

        return resp

    def login(self, username: str, password: str) -> bool:
        """
        Sends the login command to the server, to set token attribute for authentication.
        Returns if successful or not.

        Parameters
        --------
        username : str
            The `username` of the account we're logging into
        password : str
            The `password` of the account we're logging into
        """
        join_command = (r'{"join": {"username": "' +
                        username +
                        r'","password": "' +
                        password +
                        r'","token":""}}')

        response = self.send_command(join_command)

        if response.type != "error":
            self.token = response.token
            return True
        return False

    def update_bio(self, bio: str):
        """
        Sends the bio command to the server. Returns if successful or not.

        Parameters
        --------
        bio : str
            The text to update the bio into.
        """
        bio_command = (r'{"token":"' +
                       self.token +
                       r'", "bio": {"entry": "' +
                       bio +
                       r'","timestamp": "' +
                       str(time()) + r'"}}')
        response = self.send_command(bio_command)

        return response.type != "error"

    def publish_post(self, msg: str):
        """
        Sends the publish command to the server. Returns if successful or not.

        Parameters
        --------
        msg : str
            The text we wish to publish as a post to the server.
        """
        publish_command = (r'{"token":"' +
                           self.token +
                           r'", "post": {"entry": "' +
                           msg +
                           r'","timestamp": "' +
                           str(time()) +
                           r'"}}')
        response = self.send_command(publish_command)

        return response.type != "error"


def send(server, port: int, username: str, password: str, message: str, bio: str = None) -> bool:
    """
    Function creates a new Client object. Checks for bio and message args.
    If exists and nonblank, Client object will send code to run it.
    """
    client = Client(server, port)
    if not client.connect_to_server():
        print("Failed to connect to server for some reason!")
        return False
    if not client.login(username, password):
        print("Failed to login for some reason!")
        return False

    # we catch any non string message or bio
    if isinstance(message, str) and not message.isspace() and message:
        client.publish_post(message)
    else:
        print("No valid post to send.")
    if isinstance(bio, str) and not bio.isspace() and bio:
        client.update_bio(bio)
    else:
        print("No valid bio to send.")
    return True
