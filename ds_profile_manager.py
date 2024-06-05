# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

"""
temp docstring
"""

from pathlib import Path
from datetime import datetime
from time import time as get_time
from ds_profile import Profile, Post, Friend

DIRECTORY_NAME = "dsu_profiles"


class ProfileUtils:
    '''
    Class containing several methods used by multiple 
    '''
    def __init__(self, admin: bool = False) -> None:
        self.admin = admin

    def log(self, text: str, source: str, *args, error: bool = False) -> None:
        '''
        if currently in admin mode, print. otherwise, do nothing
        '''
        if self.admin:
            if error:
                header = ("Unexpected error has occured",
                          f"from <{source}> as follows:\n")
            else:
                header = f"Debug log from <{source}> as follows:\n"
            print(header + text)
            if len(args) > 0:
                print("\nAdditional objects are provided:\n")
                for i in args:
                    print(str(i) + "\n")

    def _get_post_info(self, post: Post) -> tuple:
        """
        temp docstring
        """
        content = post.get_entry()
        time = self.convert_time(post.get_time())
        return content, time

    def convert_time(self, inp_time: str, current: int = 0):
        '''
        Given a string representation of a float, convert it into a text of
        the corresponding date. If includes current, truncates timestamp
        depending on how recent the input date was.
        '''
        int_time = int(float(inp_time))
        time = datetime.fromtimestamp(int(int_time))
        if current == 0:  # full timestamp
            strtime = time.strftime('%Y/%m/%d %H:%M')
        elif current - int_time < 43200:  # only month and day
            strtime = time.strftime('%H:%M')
        elif current - int_time < 15811200:  # only month and day
            strtime = time.strftime('%M %d')
        else:  # year month day
            strtime = time.strftime('%Y/%m/%d')
        return strtime

    def _get_path(self, usn: str = None) -> Path:
        """
        Returns the path of the file of a profile's dsu file.
        """
        direc_path = Path.cwd() / Path(DIRECTORY_NAME)
        return direc_path / Path(usn + ".dsu") if usn else direc_path

    def _create_profile(self, usn: str = None, pw: str = None,
                       profile: Profile = None) -> bool:
        """
        Given a username and password, creates and saves that profile
        to a new .dsu file. If profile is given instead, saves that
        profile instead.
        """
        try:
            if profile is None:
                profile = Profile(None, usn, pw)
            path = self._get_path(profile.username)
            self.log(f"attempting to save at {path}", "create profile")
            path.touch()
            profile.save_profile(path)
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise

    def _delete_profile(self, usn: str) -> bool:
        """
        Given a username, deletes the .dsu file from the directory.
        """
        try:
            path = self._get_path(usn)
            path.unlink()
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise


    def _fetch_profiles(self) -> list[str]:
        """
        Gets the usernames from all the .dsu files from the directory.
        """
        profiles = []

        for i in self._get_path().iterdir():
            if i.is_file() and i.suffix == ".dsu":
                profiles.append(str(i.name[:-4]))
        return profiles.copy()


class DsuManager(ProfileUtils):
    """
    Manages profile creation, fetching, and deletion.
    """
    def __init__(self, admin: bool = False) -> None:
        super().__init__(admin)
        self.profile_path = self.create_profile_directory()

    def create_profile_directory(self) -> Path:
        """
        temp docstring
        """
        profile_path = self._get_path()
        if not profile_path.exists():
            profile_path.mkdir(parents=True)

        return profile_path

    def create_profile(self, usn: str = None, pw: str = None,
                       profile: Profile = None) -> bool:
        """
        temp docstring
        """
        return self._create_profile(usn, pw, profile)

    def delete_profile(self, usn: str):
        """
        if currently in admin mode, print. otherwise, do nothing
        """
        return self._delete_profile(usn)

    def fetch_profiles(self) -> list[str]:
        """
        temp docstring
        """
        return self._fetch_profiles()


class ProfileManager(ProfileUtils):
    """
    Able to manage specific profile, to access, save, verify, and
    modify server details.
    """
    def __init__(self, username: str, admin: bool = False) -> None:
        super().__init__(admin)
        self.profile_path = Path.cwd() / Path(DIRECTORY_NAME)
        self.loaded = self._init_profile(username)

    def _init_profile(self, username: str) -> bool:
        """
        temp docstring
        """
        try:
            self.log(f"Attempting to access {username}", "pm init_profile")
            self.profile = self.access_profile(username)
            self.posts = self.profile.get_posts()
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise

    def save_profile(self) -> bool:
        """
        temp docstring
        """
        try:
            path = self._get_path(self.profile.username)
            self.profile.save_profile(path)
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise

    def access_profile(self, usn: str) -> Profile:
        """
        temp docstring
        """
        path = self._get_path(usn)
        try:
            profile = Profile()
            profile.load_profile(path)
            return profile
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise

    def get_profile_info(self) -> tuple:
        """
        temp docstring
        """
        pf = self.profile
        return pf.username, pf.password, pf.bio

    def get_server_info(self) -> tuple:
        """
        temp docstring
        """
        pf = self.profile
        return pf.dsuserver[0], pf.dsuserver[1], pf.username, pf.password

    def update_server_info(self, host: str = None,
                           port: int = None, reset: bool = False):
        """
        temp docstring
        """
        try:
            self.profile.dsuserver = None if reset else (host, int(port))
            self.save_profile()
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise

    def verify_joinable(self) -> bool:
        """
        temp docstring
        """
        self.log(f"accessing dsuserver and got {self.profile.dsuserver}",
                 "pm verify joinable")
        return self.profile.dsuserver is not None

class PostManager(ProfileManager):
    '''
    Manages editing profile's bio, username, password, and posts.
    '''
    def edit_bio(self, content: str) -> bool:
        """
        temp docstring
        """
        try:
            self.profile.bio = content
            self.save_profile()
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise

    def edit_usn(self, content: str) -> bool:
        """
        Edits username of profile, and saves to new .dsu file.
        """
        if content not in self._fetch_profiles():
            self._delete_profile(self.profile.username)
            self.profile.username = content
            self._create_profile(profile=self.profile)
            return True
        self.log("Did not change usn, would override file", "pm edit usn func")
        return False

    def edit_pw(self, content: str) -> bool:
        """
        Edits password of profile and saves.
        """
        try:
            self.profile.password = content
            self.save_profile()
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise

    def create_post(self, content: str) -> str:
        """
        Given a string, we create a post and save it to the profile.
        Then we return the timestamp of the post as a string.
        """
        post = Post(content)
        self.profile.add_post(post)
        self.save_profile()
        return self._get_post_info(post)[1]

    def edit_post(self, index: int, content: str) -> bool:
        """
        Given the index of a post, replace its contents with a new
        string and save profile.
        """
        try:
            post = self.profile.get_posts()[index]
            post.set_entry(content)
            self.save_profile()
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise

    def del_post(self, index: int) -> bool:
        """
        Given the index of a post, deletes it and saves the profile.
        """
        try:
            self.profile.del_post(index)
            self.save_profile()
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise

    def index_post(self, index: int) -> tuple:
        """
        Given the index of a post, returns a tuple of the post's
        content and timestamp.
        """
        post = self.posts[index]
        content, time = self._get_post_info(post)
        return content, time

    def fetch_posts(self):
        """
        Iterable for tuple pairs of the content and timestamp of the
        profile's posts.
        """
        for i in self.posts:
            content, time = self._get_post_info(i)
            yield content, time

class DmManager(ProfileManager):
    '''
    Manages user's friends and chat messages.
    '''
    def __init__(self, username: str, admin: bool = False) -> None:
        super().__init__(username, admin)
        self.loaded_friend: Friend = None

    def _init_profile(self, username: str) -> bool:
        """
        Loads profile of specific username.
        """
        try:
            self.log(f"Attempting to access {username}", "pm init_profile")
            self.profile = self.access_profile(username)
            self.friends = self.profile.get_friends()
            return True
        except Exception as exc:
            print(f"Unexpected {exc}: {type(exc)}")
            raise

    def load_friend(self, friend: str) -> bool:
        '''
        From the loaded profile, load the DMs of a friend of that profile.
        '''
        names = [i.get_name() for i in self.friends]
        try:
            index = names.index(friend)
        except ValueError:
            return False
        self.loaded_friend = self.friends[index]
        return True

    def save_friend(self) -> bool:
        '''
        Saves the currently loaded friend and all their messages.
        '''
        names = [i.get_name() for i in self.friends]
        target_name = self.loaded_friend.get_name()
        try:
            index = names.index(target_name)
            self.friends[index] = self.loaded_friend
            self.save_profile()
        except ValueError:
            ins = self.loaded_friend.get_in_msgs()
            outs = ins = self.loaded_friend.get_out_msgs()
            self.add_friend(target_name, ins, outs)
        else:
            return True
        return False

    def fetch_friends(self) -> list[Friend]:
        '''
        Returns a list of friends the loaded profile has.
        '''
        return self.friends

    def add_friend(self, friend: str,
                   in_msg: list = None,
                   out_msg: list = None) -> str:
        """
        Given a string, we create a friend and save it to the profile.
        Then we return if successful.
        """
        new_friend = Friend(friend, out_msg, in_msg)
        self.profile.add_friend(new_friend)
        self.save_profile()
        self.loaded_friend = new_friend
        return friend

    def load_texts(self) -> list[tuple[Post, str]]:
        '''
        From the loaded friend, get all the DMs to and from, and return
        a sorted list containing tuples of the message and the sender.
        '''
        my_name = self.profile.username
        thr_name = self.loaded_friend.get_name()

        raw_me = self.loaded_friend.get_out_msgs()
        raw_thr = self.loaded_friend.get_in_msgs()

        paired_my_texts = [(i, my_name) for i in raw_me] if raw_me else []
        paired_thr_texts = [(i, thr_name) for i in raw_thr] if raw_thr else []

        paired_texts = paired_my_texts + paired_thr_texts
        paired_texts.sort(key=lambda dm: dm[0].get_time())

        return paired_texts

    def add_text(self, text: str, timestamp: float = get_time(),
                 recipient: bool = True) -> bool:
        '''
        Given a text and timestamp, adds the text to the profile's messages
        and saves.
        '''
        new_text = Post(text)
        new_text.set_time(timestamp)
        if recipient:
            current_in_msgs = self.loaded_friend.get_in_msgs()
            current_in_msgs.append(new_text)
            self.loaded_friend.set_in_msgs(current_in_msgs)
        else:
            current_out_msgs = self.loaded_friend.get_out_msgs()
            current_out_msgs.append(new_text)
            self.loaded_friend.set_out_msgs(current_out_msgs)
        self.save_friend()
