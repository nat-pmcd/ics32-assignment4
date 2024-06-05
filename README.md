# ics32-assignment4
Final project for ICS 32, wooo! Remaining tasks are to add docstrings, lint remaining files, and make the test cases.

## ds_protocol.py
Given a socket, supports sending and receiving commands to server.
Tested with test_ds_message_protocol.py

## ds_messenger.py
Contains the DirectMessenger and PostPublisher classes, to manage logging in to servers and sending pre-made commands.
DirectMessenger is tested with test_ds_messenger.py

## Profile.py
Should be modified to now also store past retrieved messages

## gui.py
GUI program, which automatically launches. Automatically retrieves messages while running, saves for offline access.