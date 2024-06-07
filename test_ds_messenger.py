# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

"""
Tests DirectMessenger and DirectMessage.
Hey, we should test private methods, right?
python -m pytest --cov=ds_messenger
"C:\Users\jonat\Downloads\python\git repos\ics32-assignment4\test_ds_messenger.py"
"""

import unittest
from time import time as get_time
from random import randrange
from ds_messenger import DirectMessenger, DirectMessage

DSU_ADDRESS = "168.235.86.101", 3021


class DirectMessageTest(unittest.TestCase):
    '''
    Unit tests for DirectMessage
    '''
    def test_set_recipient(self):
        '''
        Testing setting the recipient.
        '''
        message = DirectMessage()  # organize phase
        name = "NAME"
        message.set_recipient(name)  # action phase
        assert message.recipient == name  # assert phase

    def test_set_msg_time_spec(self):
        '''
        Testing setting the message, with a specific time.
        '''
        message = DirectMessage()  # organize phase
        time = 1.0
        contents = 'MESSAGE'
        message.set_message(contents, time)  # action phase
        assert message.timestamp == time  # assert phase
        assert message.message == contents

    def test_set_msg_time_none(self):
        '''
        Testing setting the message, with no given time.
        '''
        message = DirectMessage()  # organize phase
        time = get_time()
        contents = 'MESSAGE'
        message.set_message(contents, time)  # action phase
        assert message.timestamp - time < 1  # assert phase
        assert message.message == contents


class ConnectServerTest(unittest.TestCase):
    '''
    Unit tests for DirectMessenger connect_to_server method
    '''
    def _connect_test(self, address):
        ip, port = address
        dm_manager = DirectMessenger(ip, port)
        return dm_manager._connect_to_server()

    def test_successful_connect(self):
        '''
        Testing connecting to a valid server.
        '''
        dsu_address = DSU_ADDRESS
        google_address = "8.8.8.8", 853
        assert self._connect_test(dsu_address)
        assert self._connect_test(google_address)

    def test_failed_connect(self):
        '''
        Testing connecting to a invalid server.
        '''
        local_address = "localhost", 1
        nonsense_address = "hehehehe", "he he"
        assert not self._connect_test(local_address)
        assert not self._connect_test(nonsense_address)


class SendCommandTest(unittest.TestCase):
    '''
    Unit tests for DirectMessenger _send_command method
    '''
    def _command_test(self, command):
        ip, port = DSU_ADDRESS
        dm = DirectMessenger(ip, port)
        return dm._send_command(command).type

    def test_invalid_command(self):
        '''
        Testing sending invalid commands.
        '''
        invalid_commands = ['', 'blahblah', 1, None, r'"', '\n']
        for i in invalid_commands:
            assert self._command_test(i) == 'error'

    def test_valid_command(self):
        '''
        Testing sending invalid commands.
        '''
        usn = "s24testuser"
        pw = "123"
        i = f'{{"join":{{"username":"{usn}","password":"{pw}","token":""}}}}'
        assert self._command_test(i) == 'ok'


class VerifyNonblankTest(unittest.TestCase):
    '''
    Unit tests for DirectMessenger _verify_nonblank method
    '''
    def _blank_test(self, string):
        dm = DirectMessenger()
        return dm._verify_nonblank(string)

    def test_valid_string(self):
        '''
        Testing with valid string.
        '''
        string = "I am a string!"
        assert self._blank_test(string)

    def test_empty_string(self):
        '''
        Testing with empty string.
        '''
        string = ""
        assert not self._blank_test(string)

    def test_whitespace_string(self):
        '''
        Testing with whitespace string.
        '''
        string = "  \n  \n  "
        assert not self._blank_test(string)


class LoginTest(unittest.TestCase):
    '''
    Unit tests for DirectMessenger login method
    '''
    def _login_test(self, login: tuple[str]):
        ip, port = DSU_ADDRESS
        dm = DirectMessenger(ip, port)
        usn, pw = login
        return dm.login(usn, pw)

    def test_invalid_logins(self):
        '''
        Unit test for invalid logins
        '''
        invalid_logins = [
            ("Bob", "123"),  # wrong password
            (" ", " "),  # nonsense blank login
            ("s24testuser", "1234"),  # wrong password
            ("innocuous username", "123")  # invalid usn
        ]
        for i in invalid_logins:
            assert not self._login_test(i)

    def test_valid_logins(self):
        '''
        Unit test for valid logins
        '''
        valid_logins = [  # all profiles i've used
            ("s24testuser", "123"),
            ("s24testuser1", "123"),
            ("s24testuser2", "123"),
            ("philex", "123")
        ]
        for i in valid_logins:
            assert self._login_test(i)

    def test_new_login(self):
        '''
        Unit test for new login
        '''
        base = 's24testuser'
        random = randrange(6, 99)
        usn = base + str(random)
        pw = '12345'
        login = usn, pw
        assert self._login_test(login)


class SendFetchDmTest(unittest.TestCase):
    '''
    Unit tests for DirectMessenger Send and _fetch methods
    '''
    def _send_test(self, msg: list):
        ip, port = DSU_ADDRESS
        sender = DirectMessenger(ip, port)
        sender.login('s24testuser1', '123')

        if isinstance(msg, list):
            for i in msg:
                success = sender.send(i, 's24testuser2')
                if not success:
                    return False
        else:
            success = sender.send(msg, 's24testuser2')
            if not success:
                return False

        if not self._recv_new_test(msg):
            return False
        return True

    def _recv_new_test(self, msg: list):
        ip, port = DSU_ADDRESS
        recipient = DirectMessenger(ip, port)
        recipient.login('s24testuser2', '123')
        resp = recipient.retrieve_new()
        success = True

        if isinstance(msg, list):
            for pos, i in enumerate(msg):
                if i != resp[pos].message:
                    success = False
        else:
            success = msg == resp[0].message
        return success

    def test_no_server(self):
        '''
        Test if no server is given
        '''
        assert not DirectMessenger().send('yay', 's24testuser1')

    def test_no_sender(self):
        '''
        Test if no user is given
        '''
        ip, port = DSU_ADDRESS
        dm = DirectMessenger(ip, port)
        dm.login('', '')
        assert not dm.send('yay', 's24testuser1')

    def test_invalid_message(self):
        '''
        Test if invalid message is given.
        '''
        invalid_msgs = [
            'Heya!' + '\n' + 'How you doing?',
            '"',
            ' '
        ]
        for i in invalid_msgs:
            assert not self._send_test(i)

    def test_valid_message(self):
        '''
        Test if valid message is given.
        '''
        valid_msgs = [
            'Heya! How you doing?',
            ':)',
            'wasup',
            ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' +
             'Integer commodo lobortis condimentum. Sed id porta arcu, ' +
             'eu finibus quam. In eget sem tincidunt, luctus elit vel, ' +
             'porttitor erat. Nam erat felis, interdum porta augue eget, ' +
             'blandit convallis nisi. Nulla condimentum ante at sodales ' +
             'porta. Praesent id magna porta, faucibus eros vitae, mollis ' +
             'sem. Class aptent taciti sociosqu ad litora torquent per ' +
             'conubia nostra, per inceptos himenaeos. Cras feugiat, lacus ' +
             'sit amet accumsan volutpat, sapien augue sagittis erat, eget ' +
             'tincidunt quam ex ac est. Duis sit amet massa tellus. ')
        ]
        for i in valid_msgs:
            assert self._send_test(i), f"{i}"
        assert self._send_test(valid_msgs)


if __name__ == '__main__':
    unittest.main()
