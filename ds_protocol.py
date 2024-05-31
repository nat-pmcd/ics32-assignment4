# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

import json
import socket
from collections import namedtuple

Response = namedtuple('Response', ['response', 'type', 'message', 'token'])
Connection = namedtuple('Connection', ['socket', 'send', 'recv'])


def init(sock: socket) -> Connection:  # create connection o
    try:
        f_send = sock.makefile('w')
        f_recv = sock.makefile('r')
        print("Initiated connection")
        return Connection(sock, f_send, f_recv)
    except Exception as exc:
        print(f"Invalid socket connection, {exc}: {type(exc)}")


def send_command(conn: Connection, command: str):  # single command to send and receive response
    if send(conn, command):
        response = listen(conn)
        return response


def send(conn: Connection, command: str) -> bool:  # wrapper for send response. returns bool for if succesful in sending
    try:
        _send_response(conn, command)
        return True
    except Exception as exc:
        print(f"Unexpected {exc} when sending: {type(exc)}")
        return False


def listen(conn: Connection) -> Response:  # wrapper for receive response
    try:
        return _read_response(conn)
    except Exception as exc:
        print(f"Unexpected {exc} when listening: {type(exc)}")
        return Response(None, "error", "Error caught by client when trying to listen to server!", None)


def extract_json(json_msg: str) -> Response:  # extract server response into Response tuple
    try:
        json_obj = json.loads(json_msg)

        response = json_obj['response']  # every server response should have type and message, but not necessarily token
        type = response['type']
        message = response['message']
        token = response['token'] if 'token' in response else None

        return Response(response, type, message, token)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    except KeyError:
        print("Json isn't complete.")


def exit(conn: Connection):  # close connection
    conn.send.close()
    conn.recv.close()


def _read_response(conn: Connection) -> Response:
    try:
        response = conn.recv.readline()[:-1]
        print("received response", response)
        return extract_json(response)
    except Exception as exc:
        print(f"Unexpected {exc}: {type(exc)}")
        raise


def _send_response(conn: Connection, command: str) -> None:
    try:
        conn.send.write(command + "\r\n")
        conn.send.flush()
    except Exception as exc:
        print(f"Unexpected {exc}: {type(exc)}")
        raise
