# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

"""
Tests ds_protocol
"""

import unittest
import socket
import ds_protocol as dsp
from ds_protocol import _extract_json as extract_json

DSU_ADDRESS = "168.235.86.101", 3021


class InitTest(unittest.TestCase):
    '''
    Unit tests for dsp init and close method
    '''
    def test_init(self):
        '''
        testing with valid socket connection
        '''
        sock = _create_socket(DSU_ADDRESS)
        assert isinstance(dsp.init(sock), dsp.Connection)

    def test_not_init(self):
        '''
        testing with not a socket
        '''
        assert dsp.init('') is None

    def test_close_socket(self):
        '''
        testing close with
        '''
        sock = _create_socket(DSU_ADDRESS)
        conn = dsp.init(sock)
        assert dsp.close_conn(conn)

    def test_close_invalid(self):
        '''
        testing close with
        '''
        assert not dsp.close_conn("conn")


class ReadWriteTest(unittest.TestCase):
    '''
    Unit tests for dsp send_command method
    '''
    def test_valid_command(self):
        '''
        testing with valid command
        '''
        join_command = (r'{"join": {"username": "s24testuser1"' +
                        ',"password": "123","token":""}}')
        sock = _create_socket(DSU_ADDRESS)
        conn = dsp.init(sock)
        resp = dsp.send_command(conn, join_command)
        assert resp.message == "Welcome back, s24testuser1"


class ReadJson(unittest.TestCase):
    '''
    Unit tests for dsp _extract_json
    '''
    def test_message_json(self):
        '''
        testing with sending a direct message
        '''
        msg_type = "ok"
        msg = "Direct message sent"
        string = (f'{{"response": {{"type": "{msg_type}",' +
                  f' "message": "{msg}"}}}}').replace("'", '"')
        resp = extract_json(string)
        assert resp.type == msg_type, string
        assert resp.message == msg
        assert resp.token is None

    def test_login_json(self):
        '''
        testing with sending a login request
        '''
        msg_type = "ok"
        message = "Welcome back, s24testuser2"
        token = "6f7d13ac-772e-4ef7-aa4a-aaec5d848ae3"
        string = (f"{{'response': {{'type': '{msg_type}', 'message':" +
                  f" '{message}', 'token': '{token}'}}}}").replace("'", '"')
        resp = extract_json(string)
        assert resp.type == msg_type, "<" + string + ">"
        assert resp.message == message
        assert resp.token == token

    def test_invalid_json(self):
        '''
        testing with an invalid json
        '''
        string = 'blah blah blah'
        resp = extract_json(string)
        assert resp.type == 'error'
        assert resp.response == string
        assert resp.message == "Client error extracting json"

    def test_incomplete_json(self):
        '''
        testing with incomplete json
        '''
        string = r'{}'
        resp = extract_json(string)
        assert resp.type == 'error'
        assert resp.response == string
        assert resp.message == "Client error extracting json"

    def test_msgs_json(self):
        '''
        testing with a message request
        '''
        msg_type = 'ok'
        messages = [
            {"message": "Hello User 1!",
             "from": "markb",
             "timestamp": "1603167689.3928561"},
            {"message": "Bzzzzz",
             "from": "thebeemoviescript",
             "timestamp": "1603167689.3928561"}
        ]
        messagse_str = [str(i) for i in messages]
        msg = ", ".join(messagse_str).replace("'", '"')
        string = (f"{{'response': {{'type': '{msg_type}'," +
                  f" 'messages': [{msg}]}}}}").replace("'", '"')
        resp = extract_json(string)
        assert resp.type == msg_type, string
        for pos, message in enumerate(messages):
            for i in message:
                assert message[i] == resp.messages[pos][i]


def _create_socket(address) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    return sock


if __name__ == '__main__':
    unittest.main()
