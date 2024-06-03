# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

"""
temp docstring
"""

from pathlib import Path
from datetime import datetime
from ds_profile import Profile, Post

DIRECTORY_NAME = "dsu_profiles"

class AdminPrinter:
    """
    temp docstring
    """
    def __init__(self, admin: bool = False) -> None:
        self.admin = admin

    def log(self, text: str, source: str, *args, error: bool = False) -> None:
        '''
        if currently in admin mode, print. otherwise, do nothing
        '''
        if self.admin:
            if error:
                header = f"Unexpected error has occured from <{source}> as follows:\n"
            else:
                header = f"Debug log from <{source}> as follows:\n"
            print(header + text)
            if len(args) > 0:
                print("\nAdditional objects are provided:\n")
                for i in args:
                    print(str(i) + "\n")


class DsuManager(AdminPrinter):
    """
    temp docstring
    """
    def __init__(self, admin = False) -> None:
        super().__init__()
        self.admin = admin
        self.profile_path = self.create_profile_directory()  # first create dsu folder

    def create_profile_directory(self) -> Path:
        """
        temp docstring
        """
        profile_path = get_path()
        if not profile_path.exists():  # if the path doesn't exist, create it. otherwise do nothing
            profile_path.mkdir(parents=True)

        return profile_path

    def create_profile(self, usn: str = None, pw: str = None, profile: Profile = None) -> bool:
        """
        temp docstring
        """
        return create_profile(usn, pw, profile, self.admin)

    def delete_profile(self, usn: str, admin: bool = False):
        """
        if currently in admin mode, print. otherwise, do nothing
        """
        return delete_profile(usn, admin)

    def fetch_profiles(self) -> list[str]:
        """
        temp docstring
        """
        return fetch_profiles()


class ProfileManager(AdminPrinter):
    """
    temp docstring
    """
    def __init__(self, username: str, admin = False) -> None:
        super().__init__()
        self.admin = admin
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
            self.log("failure when opening profile", "pm init profile", type(exc), exc, error=True)
            return False

    def get_profile_info(self) -> tuple:
        """
        temp docstring
        """
        pf = self.profile
        return pf.username, pf.password, pf.bio

    def save_profile(self) -> bool:
        """
        temp docstring
        """
        try:
            path = get_path(self.profile.username)
            self.profile.save_profile(path)
            return True
        except Exception as exc:
            self.log("failure when saving profile", "pm save profile", type(exc), exc, error=True)
            return False

    def edit_bio(self, content: str) -> bool:
        """
        temp docstring
        """
        try:
            self.profile.bio = content
            self.save_profile()
            return True
        except Exception as exc:
            self.log("failure when editing bio", "pm edit bio", type(exc), exc, error=True)
            return False

    def edit_usn(self, content: str) -> bool:
        """
        temp docstring
        """
        if content not in fetch_profiles():
            delete_profile(self.profile.username)
            self.profile.username = content
            create_profile(profile=self.profile, admin=self.admin)
            return True
        self.log("Did not change usn, would override file", "pm edit usn func")
        return False

    def edit_pw(self, content: str) -> bool:
        """
        temp docstring
        """
        try:
            self.profile.password = content
            self.save_profile()
            return True
        except Exception as exc:
            self.log("failure when editing pw", "pm edit pw", type(exc), exc, error=True)
            return False

    def access_profile(self, usn: str) -> Profile:
        """
        temp docstring
        """
        path = get_path(usn)
        try:
            profile = Profile()
            profile.load_profile(path)
            return profile
        except Exception as exc:
            self.log("failure accessing profile", "pm access profile", type(exc), exc, error=True)
            return None

    def get_server_info(self) -> tuple:
        """
        temp docstring
        """
        pf = self.profile
        return pf.dsuserver[0], pf.dsuserver[1], pf.username, pf.password

    def update_server_info(self, host: str = None, port: int = None, reset: bool = False):
        """
        temp docstring
        """
        try:
            self.profile.dsuserver = None if reset else (host, int(port))
            self.save_profile()
            return True
        except Exception as exc:
            self.log("failure updating server", "pm update serv info", type(exc), exc, error=True)
            return False

    def create_post(self, content: str) -> str:  # we return the timestamp of post
        """
        temp docstring
        """
        post = Post(content)
        self.profile.add_post(post)
        self.save_profile()
        return get_post_info(post)[1]

    def edit_post(self, index: int, content: str) -> bool:
        """
        temp docstring
        """
        try:
            post = self.profile.get_posts()[index]
            post.set_entry(content)
            self.save_profile()
            return True
        except Exception as exc:
            self.log("failure when editing post", "pm edit post", type(exc), exc, error=True)
            return False

    def del_post(self, index: int) -> bool:
        """
        temp docstring
        """
        try:
            self.profile.del_post(index)
            self.save_profile()
            return True
        except Exception as exc:
            self.log("failure when deleting post", "pm del post", type(exc), exc, error=True)
            return False

    def index_post(self, index: int) -> tuple:
        """
        temp docstring
        """
        post = self.posts[index]
        content, time = get_post_info(post)
        return content, time

    def fetch_posts(self):
        """
        temp docstring
        """
        for i in self.posts:
            content, time = get_post_info(i)
            yield content, time

    def verify_joinable(self) -> bool:
        """
        temp docstring
        """
        self.log(f"accessing dsuserver and got {self.profile.dsuserver}", "pm verify joinable")
        return self.profile.dsuserver is not None


def get_post_info(post: Post) -> tuple:
    """
    temp docstring
    """
    content = post.get_entry()
    time = datetime.fromtimestamp(post.get_time()).strftime('%Y-%m-%d %H:%M:%S')
    return content, time


def get_path(usn: str = None) -> Path:
    """
    temp docstring
    """
    direc_path = Path.cwd() / Path(DIRECTORY_NAME)
    return direc_path / Path(usn + ".dsu") if usn else direc_path


def create_profile(usn: str = None, pw: str = None,
                   profile: Profile = None, admin: bool = False) -> bool:
    """
    temp docstring
    """
    logger = AdminPrinter(admin)
    try:
        if profile is None:
            profile = Profile(None, usn, pw)
        path = get_path(profile.username)
        logger.log(f"attempting to save at {path}", "create profile")
        path.touch()
        profile.save_profile(path)
        return True
    except Exception as exc:
        logger.log("failure when creating profile", "create profile", type(exc), exc, error=True)
        return False


def delete_profile(usn: str, admin: bool = False) -> bool:
    """
    temp docstring
    """
    logger = AdminPrinter(admin)
    try:
        path = get_path(usn)
        path.unlink()
        return True
    except Exception as exc:
        logger.log("failure when deleting profile", "delete profile", type(exc), exc, error=True)
        return False


def fetch_profiles() -> list[str]:
    """
    temp docstring
    """
    profiles = []

    for i in get_path().iterdir():
        if i.is_file() and i.suffix == ".dsu":
            profiles.append(str(i.name[:-4]))
    return profiles.copy()