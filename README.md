# ics32-assignment3
Current todo:
Modify ds_profile.py to be able to access and edit messages.
Update ds_profile_manager.py to get all messages, and add messages.
Update ds_gui.py to have a gui.

Write tests for ds_protocol.py
Write tests for ds_messenger.py

## ds_protocol.py
Should now also support directmessage

### Format of json
#### send to another user and response
{"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}
{"response": {"type": "ok", "message": "Direct message sent"}}

#### read unread/read messages
{"token":"user_token", "directmessage": "new"}
{"token":"user_token", "directmessage": "all"}

{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript" "timestamp":"1603167689.3928561"}]}}

## test_ds_message_protocol.py
test functionality of ds_message_protocl

## ds_messenger.py
class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
		
  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    pass
		
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    pass
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    pass

## test_ds_messenger.py
test functionality of ds_messenger

## Profile.py
Should be modified to now also store past retrieved messages

## gui.py
Should automatically retrieve new messages while program runs
Should have an identifier for recipient and sender