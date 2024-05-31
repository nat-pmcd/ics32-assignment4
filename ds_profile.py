# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

"""
Profile.py

ICS 32
Assignment #2: Journal

Author: Mark S. Baldwin, modified by Alberto Krone-Martins

v0.1.9
"""

import json
import time
from pathlib import Path

class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to load or save Profile objects to file the system.
    """


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to deserialize a dsu file to a Profile object.
    """


class Post(dict):
    """ 
    The Post class is responsible for working with individual user posts. It currently 
    supports two features: A timestamp property that is set upon instantiation and 
    when the entry object is set and an entry property that stores the post message.

    """
    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        """
        Sets the post's self to the given parameter 
        """
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self) -> str:
        """
        Returns the entry property as a string
        """
        return self._entry

    def set_time(self, time_input: float):
        """
        Sets the post's time to the given float parameter
        """
        self._timestamp = time_input
        dict.__setitem__(self, 'timestamp', time_input)

    def get_time(self) -> float:
        """
        Returns the time property of the entry as a float.
        """
        return self._timestamp

    # The property method is used to support get and set capability for entry and
    # time values. When the value for entry is changed, or set, the timestamp field is
    # updated to the current time.
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Friend(dict):
    """
    The Friend class is responsible for working with the friends a user may have.
    """
    def __init__(self, name: str = None,
                 sent_messages: list[Post] = None,
                 recv_messages: list[Post] = None) -> None:
        self._name = name
        self.set_out_msgs(sent_messages)
        self.set_in_msgs(recv_messages)

        # Wondering how the hell this black magic works now...
        dict.__init__(self, name=self._name, in_posts=self._in_msgs, out_posts=self._out_msgs)

    def get_name(self) -> str:
        """
        Returns the name property as a string
        """
        return self._name

    def set_name(self, usn: str):
        """
        Sets the name property to argument
        """
        self._name = usn
        dict.__setitem__(self, 'name', usn)

    def get_out_msgs(self) -> list[Post]:
        """
        Returns the list of your messages
        """
        return self._out_msgs

    def get_in_msgs(self) -> list[Post]:
        """
        Returns the list of their messages
        """
        return self._in_msgs

    def set_out_msgs(self, out_msgs: list[Post]):
        """
        Returns the list of your messages
        """
        self._out_msgs = out_msgs.copy()
        dict.__setitem__(self, 'timestamp', out_msgs.copy())

    def set_in_msgs(self, in_msgs: list[Post]):
        """
        Returns the list of their messages
        """
        self._in_msgs = in_msgs.copy()
        dict.__setitem__(self, 'timestamp', in_msgs.copy())

    name = property(get_name, set_name)
    out_msgs = property(get_out_msgs, set_out_msgs)
    in_msgs = property(get_in_msgs, set_in_msgs)


class Profile(dict):
    """
    The Profile class exposes the properties required to join an ICS 32 DSU server. You 
    will need to use this class to manage the information provided by each new user 
    created within your program for a2. Pay close attention to the properties and 
    functions in this class as you will need to make use of each of them in your program.

    When creating your program you will need to collect user input for the properties 
    exposed by this class. A Profile class should ensure that a username and password 
    are set, but contains no conventions to do so. You should make sure that your code 
    verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ''
        self._posts = []
        self._friends = []

    def add_post(self, post: Post) -> None:
        """
        add_post accepts a Post object as parameter and appends it to the posts list. Posts 
        are stored in a list object in the order they are added. So if multiple Posts objects 
        are created, but added to the Profile in a different order, it is possible for the 
        list to not be sorted by the Post.timestamp property. So take caution as to how you 
        implement your add_post code.
        """
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        """
        del_post removes a Post at a given index and returns True if successful and False if 
        an invalid index was supplied. 

        To determine which post to delete you must implement your own search operation on 
        the posts returned from the get_posts function to find the correct index.
        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        """
        get_posts returns the list object containing all posts that have been added to the 
        Profile object
        """
        return self._posts

    def add_friend(self, friend: Friend) -> None:
        """
        add_friend accepts a Friend object as parameter and appends it to the friend list. Friends 
        are stored in a list object in the order they are added. So if multiple Friend objects 
        are created, but added to the Profile in a different order, it is possible for the 
        list to not be sorted by the Post.timestamp property. So take caution as to how you 
        implement your add_friend code.
        """
        self._friends.append(friend)

    def del_friend(self, index: int) -> bool:
        """
        del_friend removes a Friend at a given index and returns True if successful and False if 
        an invalid index was supplied. 

        To determine which friend to delete you must implement your own search operation on 
        the posts returned from the get_friend function to find the correct index.
        """
        try:
            del self._friends[index]
            return True
        except IndexError:
            return False

    def get_friends(self) -> list[Friend]:
        """
        get_friends returns the list object containing all friends that have been added to the 
        Profile object
        """
        return self._posts

    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current instance of Profile 
        to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w', encoding="utf8")
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex) from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """
        load_profile will populate the current instance of Profile with data stored in a 
        DSU file.

        Example usage: 

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r', encoding="utf8")
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self._posts += self._get_json_posts(obj['_posts'])
                if '_friends' in obj:  # testing if we have any friends :(
                    for friend_obj in obj['_friends']:
                        name = friend_obj['name']
                        sent_messsages = self._get_json_posts(friend_obj['_out_msgs'])
                        recv_messages = self._get_json_posts(friend_obj['_in_msgs'])
                        friend = Friend(name, sent_messsages, recv_messages)
                        self._friends.append(friend)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex) from ex
        else:
            raise DsuFileError()

    def _get_json_posts(self, obj):
        """
        Given a readable like object from json, return all posts from it.
        """
        posts = []
        for post_obj in obj:
            post = Post(post_obj['entry'], post_obj['timestamp'])
            posts.append(post)
        return posts.copy()
