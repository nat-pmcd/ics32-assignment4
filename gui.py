# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

# pylint: disable = no-name-in-module
from typing import Callable
from PySide6.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem,
    QPushButton, QWidget, QInputDialog, QLabel, QGridLayout)
from PySide6.QtCore import Qt
from ProfileManager import ProfileManager, AdminPrinter
from ds_messenger import DirectMessenger as Client

# HEADER LOCALIZATION
TEXT_HEADER_PROFILE = 'Profiles'
TEXT_HEADER_ACCESS = 'Access Profiles'
TEXT_HEADER_DELETE = 'Delete Profiles'
TEXT_BUTTON_ADMIN = 'Toggle Debug'
TEXT_BUTTON_MODIFY_LOGIN = 'Modify Login'

WINDOW_TITLE_MAIN = 'DSU Client'
WINDOW_TITLE_PROF = 'DSU Client'

# PROFILE LOCALIZATION
TEXT_BUTTON_CREATE_PROFILE = 'Create Profile'
TEXT_BUTTON_ACCESS_PROFILE = 'Access'
TEXT_BUTTON_DELETE_PROFILE = 'Delete'

# CREATE PROFILE LOCALIZATION
TEXT_POPUP_CREATE_PROFILE = 'Create a profile'
TEXT_POPUP_PROMPT_NAME = 'Enter a username'
TEXT_POPUP_PROMPT_NAME_BLANK = 'Username cannot be empty'
TEXT_POPUP_PROMPT_NAME_DUPLICATE = "Username already used"
TEXT_POPUP_PROMPT_PW = 'Enter a password'
TEXT_POPUP_PROMPT_PW_BLANK = 'Password cannot be empty'

# BIO LOCALIZATION
TEXT_BUTTON_EDIT_BIO = 'Edit bio'
TEXT_BUTTON_PUBLISH_BIO = 'Publish bio'
TEXT_BUTTON_PUBLISH_BIO_UNJOINED = 'Join server'

TEXT_POPUP_EDIT_BIO = 'Edit bio'
TEXT_POPUP_PROMPT_BIO = 'Describe yourself here!'
TEXT_POPUP_PROMPT_BIO_BLANK = 'Bio cannot be empty!'

# GET SERVER LOCALIZATION
TEXT_POPUP_GET_SERVER = 'Select server (DEFAULT )'
TEXT_POPUP_PROMPT_IP = 'Enter the server IP address. Default 168.235.86.101'
TEXT_POPUP_PROMPT_IP_BLANK = 'IP address cannot be blank!'
TEXT_POPUP_PROMPT_PORT = 'Enter the server port. Default 3021'
TEXT_POPUP_PROMPT_PORT_BLANK = 'Port cannot be blank!'

# USER POST LOCALIZATION
TEXT_BUTTON_CREATE_POST = 'Create Post'
TEXT_BUTTON_EDIT_POST = 'Edit'
TEXT_BUTTON_PUBLISH_POST = 'Publish'
TEXT_BUTTON_DELETE_POST = 'Delete'

TEXT_POPUP_CREATE_POST = 'Create a post'
TEXT_POPUP_PROMPT_CONTENT = 'Write your thoughts here!'
TEXT_POPUP_PROMPT_CONTENT_BLANK = 'Cannot make an empty post!'

# EDIT POST LOCALIZATION
TEXT_POPUP_EDIT_POST = 'Edit this post'
TEXT_POPUP_PROMPT_EDIT = 'Previous post:\n'
TEXT_POPUP_PROMPT_EDIT_BLANK = TEXT_POPUP_PROMPT_CONTENT_BLANK


# USER PROMPTS
class UserPrompt(QInputDialog):
    """
    """
    def __init__(self, window_name: str, prompt_text: str, empty_text: str) -> None:
        super().__init__()
        self.setWindowTitle(window_name)
        self.setLabelText(prompt_text)
        self.empty_text = empty_text

    def get_response(self):
        while True:
            if self.exec():
                if self.check_blanks():
                    self.setLabelText(self.empty_text)
                else:
                    return self.textValue()
            else:
                return None

    def check_blanks(self) -> bool:
        return not self.textValue() or self.textValue().isspace()


class UniquePrompt(UserPrompt):
    def __init__(self, window_name: str, prompt_text: str, empty_text: str, dupe_text: str, lst: tuple) -> None:
        super().__init__(window_name, prompt_text, empty_text)
        self.dupe_text = dupe_text
        self.dupe_list = lst

    def get_response(self):
        while True:
            temp = self.exec()
            if temp:
                if self.check_blanks():
                    self.setLabelText(self.empty_text)
                elif self.check_duplicate(self.dupe_list):
                    self.setLabelText(self.dupe_text)
                else:
                    return self.textValue()
            else:
                return None

    def check_duplicate(self, lst) -> bool:
        return self.textValue() in lst


# MAIN PROFILE MENU
class ProfileMenu(QWidget, AdminPrinter):
    def __init__(self):
        super().__init__()
        self.profile_manager = ProfileManager()
        self.profiles = self.profile_manager.fetch_profiles()
        self.loaded_windows = {}
        self.fuck = [self.admin]

        self.treeWidget = QTreeWidget()  # create table with 3 columns, blank label
        self.treeWidget.setColumnCount(3)
        self.treeWidget.setHeaderLabels([TEXT_HEADER_PROFILE, TEXT_HEADER_ACCESS, TEXT_HEADER_DELETE])

        for i in self.profiles:  # for every name in profile, create a new row in the table
            self.create_row(i)

        add_row_button = QPushButton(TEXT_BUTTON_CREATE_PROFILE)
        add_row_button.clicked.connect(self.create_profile_handler)

        admin_button = QPushButton(TEXT_BUTTON_ADMIN)
        admin_button.clicked.connect(self.admin_toggle_handler)

        layout = QGridLayout(self)
        layout.addWidget(add_row_button, 0, 0)
        layout.addWidget(admin_button, 0, 2)
        layout.addWidget(self.treeWidget, 1, 0, 1, 3)
        self.setLayout(layout)

    def create_row(self, name: str) -> None:  # given a name, create an additional row in the list of profiles
        item = QTreeWidgetItem(self.treeWidget, [name])
        access_button = QPushButton(TEXT_BUTTON_ACCESS_PROFILE, self)
        access_button.clicked.connect(self.generate_button_handler(1, name))
        self.treeWidget.setItemWidget(item, 1, access_button)

        delete_button = QPushButton(TEXT_BUTTON_DELETE_PROFILE, self)
        delete_button.clicked.connect(self.generate_button_handler(2, name, item))
        self.treeWidget.setItemWidget(item, 2, delete_button)

    def admin_toggle_handler(self) -> None:
        print(f'Toggling admin, it is now {"off" if self.admin else "on"}')
        print("Note, will need to refresh any profile viewers to see changes.")
        self.admin = not self.admin
        self.fuck[0] = self.admin

    def create_profile_handler(self) -> None:
        '''
        Prompt the user via dialog boxes for a username and password.
        Once both are received, create a new profile, and add it to the list.
        '''
        username = UniquePrompt(TEXT_POPUP_CREATE_PROFILE,
                                TEXT_POPUP_PROMPT_NAME,
                                TEXT_POPUP_PROMPT_NAME_BLANK,
                                TEXT_POPUP_PROMPT_NAME_DUPLICATE,
                                tuple(self.profiles)).get_response()

        if username:
            password = UserPrompt(TEXT_POPUP_CREATE_PROFILE,
                                  TEXT_POPUP_PROMPT_PW,
                                  TEXT_POPUP_PROMPT_NAME_BLANK).get_response()
            if password:
                self.create_row(username)
                self.profiles.append(username)
                self.profile_manager.create_profile(username, password)  # FIXME: We should give feedback to the user if successful or not

    def generate_button_handler(self, type: int, value: str, item: QTreeWidgetItem = None) -> Callable[..., None]:  # generate functions to load and delete profiles
        parent = self.treeWidget
        profiles = self.profiles
        pm = self.profile_manager
        loaded_windows = self.loaded_windows
        fuck = self.fuck
        match type:
            case 1:
                def handler():
                    if value in loaded_windows:
                        self.log(f"Already loaded {value}.", "access profile button handler")
                    profile_viewer = ProfileWindow(value, fuck[0])
                    if profile_viewer.loaded:
                        profile_viewer.resize(600, 500)
                        profile_viewer.setWindowTitle(WINDOW_TITLE_PROF)
                        profile_viewer.show()
                        self.log(f"Viewing {value}", "access profile button handler")
                        loaded_windows[value] = profile_viewer
                    else:
                        self.log(f"Unable to load {value}.", "access profile button handler")
            case 2:
                def handler():
                    if pm.delete_profile(value):
                        index = parent.indexOfTopLevelItem(item)  # get the index of the current item, aka the row
                        self.log(f"successfully deleted {value} at {index}", "delete profile button handler")
                        parent.takeTopLevelItem(index)  # via the tree widget parent, remove at that index
                        profiles.remove(value)
                        if value in loaded_windows:
                            loaded_windows[value].close()  # with this, we can automatically close the profile we delete
                    else:
                        pass  # FIXME: We should give feedback to the user if succesful or not
        return handler


# PROFILE VIEWER
class ProfileWindow(QWidget, AdminPrinter):
    def __init__(self, name: str, admin: bool = False) -> None:
        super().__init__()
        self.admin = admin
        self.treeWidget = QTreeWidget()  # create table with 5 columns, 2 for info and 3 for buttons
        self.treeWidget.setColumnCount(5)
        self.treeWidget.setHeaderLabels(['Post', 'Timestamp', 'Edit', 'Publish', 'Delete'])

        self.profile_manager = ProfileManager(name, self.admin)  # handler for if unabe to load profile 
        if not self.profile_manager.loaded:
            self.loaded = False
            return
        self.loaded = True

        add_row_button = QPushButton(TEXT_BUTTON_CREATE_POST)
        add_row_button.clicked.connect(self.create_post_handler)

        usn, pw, bio = self.profile_manager.get_profile_info()
        name_label = QLabel("Username: " + usn)
        pw_label = QLabel("Password: " + pw)
        self.bio_label = QLabel("Bio: " + bio)

        edit_bio_button = QPushButton(TEXT_BUTTON_EDIT_BIO)
        edit_bio_button.clicked.connect(self.edit_bio_handler)

        joinable = self.profile_manager.verify_joinable()
        text = TEXT_BUTTON_PUBLISH_BIO if joinable else TEXT_BUTTON_PUBLISH_BIO_UNJOINED
        self.join_button = QPushButton(text)
        self.join_button.clicked.connect(self.generate_button_handler(4))

        edit_login_button = QPushButton(TEXT_BUTTON_MODIFY_LOGIN)
        edit_login_button.clicked.connect(self.edit_login_handler)

        for i, j in self.profile_manager.fetch_posts():  # for every post in the profile, create a new row in the table
            self.log(f"Creating row with content {i} and time {j}", "profile viewer init")
            self.create_row(i, j, joinable)  # i is a tuple with content and time

        layout = QGridLayout(self)
        layout.addWidget(name_label, 0, 0)
        layout.addWidget(pw_label, 0, 1, Qt.AlignCenter)
        layout.addWidget(self.bio_label, 0, 2, Qt.AlignRight)
        layout.addWidget(add_row_button, 1, 0)
        layout.addWidget(self.join_button, 1, 1)
        layout.addWidget(edit_bio_button, 1, 2)
        if self.admin: layout.addWidget(edit_login_button, 1, 3)
        layout.addWidget(self.treeWidget, 2, 0, 1, 4 if self.admin else 3)
        self.setLayout(layout)

    def create_row(self, content: str, time: str, joinable: bool = True) -> None:  # given a name, create an additional row in the list of posts
        item = QTreeWidgetItem(self.treeWidget, [content])
        self.treeWidget.setItemWidget(item, 1, QLabel(time))

        edit_button = QPushButton(TEXT_BUTTON_EDIT_POST, self)
        edit_button.clicked.connect(self.generate_button_handler(1, item=item))
        self.treeWidget.setItemWidget(item, 2, edit_button)

        publish_button = QPushButton(TEXT_BUTTON_PUBLISH_POST, self)
        publish_button.clicked.connect(self.generate_button_handler(3, item=item))
        publish_button.setEnabled(joinable)
        self.treeWidget.setItemWidget(item, 3, publish_button)

        delete_button = QPushButton(TEXT_BUTTON_DELETE_POST, self)
        delete_button.clicked.connect(self.generate_button_handler(2, item=item))
        self.treeWidget.setItemWidget(item, 4, delete_button)

    def create_post_handler(self) -> None:
        content = UserPrompt(TEXT_POPUP_CREATE_POST,
                             TEXT_POPUP_PROMPT_CONTENT,
                             TEXT_POPUP_PROMPT_CONTENT_BLANK).get_response()
        if content:
            self.log(f"attempting to add {content}", "create post button handler")
            time = self.profile_manager.create_post(content)
            joinable = self.profile_manager.verify_joinable()
            self.create_row(content, time, joinable)

    def edit_bio_handler(self) -> None:
        bio = UserPrompt(TEXT_POPUP_EDIT_BIO,
                         TEXT_POPUP_PROMPT_BIO,
                         TEXT_POPUP_PROMPT_BIO_BLANK).get_response()
        if bio:
            self.profile_manager.edit_bio(bio)
            self.bio_label.setText("Bio: " + bio)

    def edit_login_handler(self) -> None:
        username = UserPrompt(TEXT_POPUP_CREATE_PROFILE,
                                TEXT_POPUP_PROMPT_NAME,
                                TEXT_POPUP_PROMPT_NAME_BLANK).get_response()
        if username:
            self.profile_manager.edit_usn(username)

        password = UserPrompt(TEXT_POPUP_CREATE_PROFILE,
                              TEXT_POPUP_PROMPT_PW,
                              TEXT_POPUP_PROMPT_NAME_BLANK).get_response()
        if password:
            self.profile_manager.edit_pw(password)

        self.log("successfully made changes, reload whole gui to view", "modify usn/pw button handler")

    def generate_button_handler(self, type: int, item: QTreeWidgetItem = None) -> Callable[..., None]:  # generate functions to load, delete, and publish posts
        parent = self.treeWidget  # FIXME: EVERYTHING HERE
        pm = self.profile_manager
        get_all_items = ProfileWindow.get_all_items

        match type:
            case 1:  # editing a post
                def handler():
                    index = ProfileWindow.get_index(parent, item)
                    post = pm.index_post(index)
                    content = UserPrompt(TEXT_POPUP_EDIT_POST,
                                         TEXT_POPUP_PROMPT_EDIT + post[0],
                                         TEXT_POPUP_PROMPT_EDIT_BLANK).get_response()
                    if content:
                        pm.edit_post(index, content)
                        parent.setItemWidget(item, 0, QLabel(content))

            case 2:  # deleting a post
                def handler():
                    index = ProfileWindow.get_index(parent, item)
                    parent.takeTopLevelItem(index)  # via the tree widget parent, remove at that index
                    pm.del_post(index)
                    self.log(f"successfully post at {index}", "delete post button handler")
            case 3:  # publishing a post
                def handler():  # first fetch mandatory send commands
                    index = ProfileWindow.get_index(parent, item)
                    post = pm.index_post(index)
                    server, port, username, password = pm.get_server_info()
                    client = Client(server, port)
                    if client.login(username, password):
                        client.publish_post(post[0])
            case 4:   # publishing a bio
                def handler():
                    if not pm.verify_joinable():  # this disgusting code gets a server
                        host = UserPrompt(TEXT_POPUP_GET_SERVER,
                                          TEXT_POPUP_PROMPT_IP,
                                          TEXT_POPUP_PROMPT_IP_BLANK).get_response()
                        if host:
                            port = UserPrompt(TEXT_POPUP_GET_SERVER,
                                              TEXT_POPUP_PROMPT_PORT,
                                              TEXT_POPUP_PROMPT_PORT_BLANK).get_response()
                            if port:
                                self.log(f"got host:port {host}:{port}", "join button handler")
                                if not pm.update_server_info(host, port):
                                    return
                            else:
                                return
                        else:
                            return
                    server, port, username, password = pm.get_server_info()
                    bio = pm.get_profile_info()[2]
                    client = Client(server, port)
                    if client.login(username, password):
                        if not client.update_bio(bio):
                            # if we fail to connect, set dsuserver back to nothing
                            pm.update_server_info(reset=True)
                            self.log(f"failed to join server {server}:{port}",
                                     "join button handler", True, username, password)
                    else:
                        items = get_all_items(parent)
                        for i in items:
                            parent.itemWidget(i, 3).setEnabled(True)
        return handler

    def get_all_items(tree) -> list:  # try get all widgets
        items = []
        for i in range(tree.topLevelItemCount()):
            items.append(tree.topLevelItem(i))
        return items

    def get_index(parent: QTreeWidget, item: QTreeWidgetItem) -> int:
        index = parent.indexOfTopLevelItem(item)
        return index

def main_gui():
    app = QApplication([])

    window = ProfileMenu()
    window.resize(600, 500)
    window.setWindowTitle(WINDOW_TITLE_MAIN)
    window.show()
    app.exec()
    app.quit()


if __name__ == '__main__':
    print('Welcome to the ICS32 Distributed Social Client! Launching GUI...')
    main_gui()
