# ics32-assignment4
Final project for ICS 32, wooo! Opens a profile browser, which you may select a profile to either publish posts, send messages, or delete the profile.

## ds_protocol.py
Given a socket, supports sending and receiving commands to server.
Test with python -m pytest --cov=ds_protocol --cov-report=term-missing test_ds_protocol.py
Note, testing does not cover no internet statements, hence 81% coverage.

## ds_messenger.py
Contains the DirectMessenger and PostPublisher classes, to manage logging in to servers and sending pre-made commands.
Test with python -m pytest --cov=ds_messenger  --cov-report=term-missing test_ds_messenger.py
Note, testing only covers DirectMessage and DirectMessesnger. The file also contains code for a3 post publishing, hence the poor coverage. Ignoring that, it would have 81% coverage as well.

## Profile.py
Should be modified to now also store past retrieved messages

## gui.py
GUI program, which automatically launches. Automatically retrieves messages while running, saves for offline access.

## Some questions...
I violate using snake_case for certain methods, since I'm redefining parent methods which originate from C. Is this alright?
Is the terminal output important at all? OR can we print whatever we'd like there?
The assignment page mentions "dealing with possible exceptions and errors that may happen." If an error happens during runtime but which does not negatively affect the user experience, will this result in a penalty still?
Do we need to submit with a Git and README as per the rubric?
What's the expected behavior of DirectMessenger.retrieve_new() if we logged in with incorrect credentials? None? False? Error? Doesn't matter?
What should we test? Obviously ds_protocol and ds_messenger. But what about file storage, like with Profile or saving to .dsu files? Or the GUI?