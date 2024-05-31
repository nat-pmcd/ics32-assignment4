# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

import ds_protocol as dsp
import socket
from time import time
PORT = 6000
SERVER = "localhost"


class Client:
    def __init__(self, server: str = SERVER, port: int = PORT) -> None:
        self.server = server
        self.port = port
        self.token = None
        self.socket = None

    def connect_to_server(self) -> None:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            address = self.server, self.port
            self.socket.connect(address)
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            return False

    def send_command(self, command: str):
        self.connect_to_server()
        if not self.socket:
            print("Could not connect to server.")
            return

        conn = dsp.init(self.socket)
        resp = dsp.send_command(conn, command)
        print("Sent", command, "and received", resp)
        dsp.exit(conn)

        if resp.type == "error":
            print(f"Error occured when sending command! {resp.message}")

        return resp

    def login(self, username: str, password: str) -> bool:    # attempt to join the server. return if successful or not
        join_command = r'{"join": {"username": "' + username + r'","password": "' + password + r'","token":""}}'
        response = self.send_command(join_command)

        if response.type != "error":
            self.token = response.token
            return True
        return False

    def update_bio(self, bio: str):    # FIXME: redundant code, create function able to do both bio and message
        bio_command = r'{"token":"' + self.token + r'", "bio": {"entry": "' + bio + r'","timestamp": "' + str(time()) + r'"}}'
        response = self.send_command(bio_command)

        return response.type != "error"

    def publish_post(self, msg: str):
        publish_command = r'{"token":"' + self.token + r'", "post": {"entry": "' + msg + r'","timestamp": "' + str(time()) + r'"}}'
        response = self.send_command(publish_command)

        return response.type != "error"


def send(server: str, port: int, username: str, password: str, message: str, bio: str = None) -> bool:    # if we are able to connect, we return true
    client = Client(server, port)
    if not client.connect_to_server():
        print("Failed to connect to server for some reason!")
        return False
    if not client.login(username, password):
        print("Failed to login for some reason!")
        return False

    if type(message) is str and not message.isspace() and message:    # we catch any non string message or bio
        client.publish_post(message)
    else:
        print("No valid post to send.")
    if type(bio) is str and not bio.isspace() and bio:
        client.update_bio(bio)
    else:
        print("No valid bio to send.")
    return True
