# ics32-assignment4
Final project for ICS 32, wooo! All that's left is making the test cases.

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

## Some questions...
I violate using snake_case for certain methods, since I'm redefining parent methods which originate from C. Is this alright?
Is the terminal output important at all? OR can we print whatever we'd like there?
The assignment page mentions "dealing with possible exceptions and errors that may happen." If an error happens during runtime but which does not negatively affect the user experience, will this result in a penalty still?
Do we need to submit with a Git and README as per the rubric?