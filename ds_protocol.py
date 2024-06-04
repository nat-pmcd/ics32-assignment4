# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

"""
Protocol to receive and send raw data via socket.
"""

import json
import socket
from collections import namedtuple

Response = namedtuple('Response', ['response', 'type', 'message', 'token'])
Connection = namedtuple('Connection', ['socket', 'send', 'recv'])


def init(sock: socket) -> Connection:
    """
    Given a socket, return a connection tuple with socket, send, and receive
    attributes.

    Parameters
    --------
    sock : socket
        The socket which will make the read and write files.
    """
    try:
        f_send = sock.makefile('w')
        f_recv = sock.makefile('r')
        print("Initiated connection")
        return Connection(sock, f_send, f_recv)
    except OSError as exc:
        print(f"Invalid socket connection, {exc}: {type(exc)}")
        return None


def send_command(conn: Connection, command: str) -> Response:
    """
    Acts as a wrapper to send the command via conn.
    Once sends the command, awaits and returns server response.

    Parameters
    --------
    conn : Connection
        Connection object to send and receive data with.
    command : str
        The `command` we're sending the server.
    """
    if _send_response(conn, command):
        response = listen(conn)
        return response
    return None


def listen(conn: Connection) -> Response:  # wrapper for receive response
    """
    Acts as a wrapper to receive response via conn.

    Parameters
    --------
    conn : Connection
        Connection object to receive data with
    """
    try:
        return _read_response(conn)
    except TimeoutError as exc:
        print(f"Unexpected {exc} when listening: {type(exc)}")
        return Response(None, "error", "Server timed out!", None)


def _extract_json(json_msg: str) -> Response:
    """
    Given some json string, unpacks and returns it into a Response tuple.

    Parameters
    --------
    json_msg : str
        The json string we're unpacking
    """
    try:
        json_obj = json.loads(json_msg)

        response = json_obj['response']
        message_type = response['type']
        message = response['message'] if 'message' in response else response['messages']
        token = response['token'] if 'token' in response else None

        return Response(response, message_type, message, token)
    except json.JSONDecodeError:
        print("Json cannot be decoded.", json_msg)
    except KeyError:
        print("Json isn't complete.")
    return Response(json_msg, "error", "Client error extracting json", None)


def close_conn(conn: Connection) -> bool:
    """
    Function to close a conn's read and write files.

    Parameters
    --------
    conn : Connection
        The connection to close.
    """
    conn.send.close()
    conn.recv.close()


def _read_response(conn: Connection) -> Response:
    """
    Given a connection, read via the read file of the socket.
    Return the server response.

    Parameters
    --------
    conn : Connection
        The connection we're reading from.
    """
    try:
        response = conn.recv.readline()[:-1]
        # print("received response", response)

        return _extract_json(response)
    except Exception as exc:
        print(f"Unexpected {exc}: {type(exc)}")
        raise


def _send_response(conn: Connection, command: str) -> bool:
    """
    Given a connection, send text via the write file of the socket.
    Return if successful or not.

    Parameters
    --------
    conn : Connection
        The connection we're sending with.
    """
    try:
        conn.send.write(command + "\r\n")
        conn.send.flush()
        return True
    except OSError as exc:
        print(f"Unexpected {exc}: {type(exc)}")
        return False
