# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

# pylint: disable = no-name-in-module

'''
Docstring
'''

from typing import Callable
from PySide6.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem,
    QPushButton, QWidget, QLabel, QGridLayout, QPlainTextEdit)
from PySide6.QtCore import Qt
from ds_profile_manager import DsuManager, PostManager, DmManager
from ds_messenger import PostPublisher as Client
from gui_prompts import PromptGenerator as pg
from gui_prompts import TxtDsu, TxtPrf, TxtMsg

MAIN_WIDTH = 450
MAIN_HEIGHT = 400

# MAIN PROFILE MENU
class ProfileMenu(QWidget):
    '''
    Ttemp docstring
    '''
    def __init__(self):
        super().__init__()
        self.dsu_manager = DsuManager()
        self.profiles = self.dsu_manager.fetch_profiles()
        self.loaded_profiles = {}
        self.loaded_dms = {}
        self._draw()

    def _draw(self) -> None:
        self.profile_table = QTreeWidget()  # create a table w 3 cols
        self.profile_table.setColumnCount(4)
        self.profile_table.setHeaderHidden(True)

        for i in self.profiles:  # for every profile, create a row
            self._create_row(i)

        add_row_button = QPushButton(TxtDsu.BUTTON_CREATE_PROFILE)
        add_row_button.clicked.connect(self.create_profile_handler)

        layout = QGridLayout(self)
        layout.addWidget(add_row_button, 0, 0)
        layout.addWidget(self.profile_table, 1, 0, 1, 2)
        self.setLayout(layout)

    def _create_row(self, name: str) -> None:
        '''
        Create an additional row containing the name of the profile.
        Adds functional buttons to the rows to access or delete

        Parameters
        --------
        content : str
            The contents of the post.
        time : str
            The timestamp of the post, as already formatted text.
        '''
        item = QTreeWidgetItem(self.profile_table, [name])
        access_button = QPushButton(TxtDsu.BUTTON_ACCESS_PROFILE, self)
        access_button.clicked.connect(self._generate_button_handler(1, name))
        self.profile_table.setItemWidget(item, 1, access_button)

        chat_button = QPushButton(TxtDsu.BUTTON_MESSAGES_PROFILE, self)
        chat_button.clicked.connect(self._generate_button_handler(3, name))
        self.profile_table.setItemWidget(item, 2, chat_button)

        delete_button = QPushButton(TxtDsu.BUTTON_DELETE_PROFILE, self)
        delete_button.clicked.connect(
            self._generate_button_handler(2, name, item))
        self.profile_table.setItemWidget(item, 3, delete_button)

    # def admin_toggle_handler(self) -> None:  DEPRECATED, admin disabled
        # print(f'Toggling admin, it is now {"off" if self.admin else "on"}')
        # print("Note, refresh any profile viewers to see changes.")
        # self.admin = not self.admin
        # self.fuck[0] = self.admin

    def create_profile_handler(self) -> None:
        '''
        Prompt the user via dialog boxes for a username and password.
        Once both are received, create a new profile, and add it to the list.
        '''
        duplicates = tuple(self.profiles)
        username = pg().get_username_prompt(duplicates).get_response()

        if not username:
            return
        password = pg().get_password_prompt().get_response()
        if not password:
            return
        self._create_row(username)
        self.profiles.append(username)
        self.dsu_manager.create_profile(username, password)
        return  # Should give feedback to the user if successful or not

    def _generate_button_handler(self, version: int, value: str,
                                 item: QTreeWidgetItem = None
                                 ) -> Callable[..., None]:
        parent = self.profile_table
        profiles = self.profiles
        pm = self.dsu_manager
        loaded_profiles = self.loaded_profiles
        loaded_dms = self.loaded_dms
        match version:
            case 1:
                def access_profile_handler():
                    if value in loaded_profiles:
                        pm.log(f"Already loaded {value}.",
                               "access profile button handler")
                    profile_viewer = ProfileWindow(value)
                    if profile_viewer.loaded:
                        profile_viewer.resize(600, 500)
                        profile_viewer.setWindowTitle(TxtPrf.WINDOW_PROFILE)
                        profile_viewer.show()
                        pm.log(f"Viewing {value}",
                               "access profile button handler")
                        loaded_profiles[value] = profile_viewer
                    else:
                        pm.log(f"Unable to load {value}.",
                               "access profile button handler")
                return access_profile_handler
            case 2:
                def delete_profile_handler():
                    if pm.delete_profile(value):
                        index = parent.indexOfTopLevelItem(item)  # get row
                        pm.log(f"successfully deleted {value} at {index}",
                               "delete profile button handler")
                        parent.takeTopLevelItem(index)  # remove at index
                        profiles.remove(value)
                        if value in loaded_profiles:  # close deleted profile
                            loaded_profiles[value].close()
                        if value in loaded_dms:
                            loaded_dms[value].close()
                    else:
                        pass  # Should give feedback to the user
                return delete_profile_handler
            case 3:
                def access_messenger_handler():
                    if value in loaded_dms:
                        pm.log(f"Already loaded {value}.",
                               "access messenger button handler")
                    messenger = MessengerWindow(value)
                    if messenger.loaded:
                        messenger.resize(600, 500)
                        messenger.setWindowTitle(TxtPrf.WINDOW_PROFILE)
                        messenger.show()
                        pm.log(f"Viewing {value}",
                               "access messenger button handler")
                        loaded_dms[value] = messenger
                    else:
                        pm.log(f"Unable to load {value}.",
                               "access messenger button handler")
                return access_messenger_handler


# PROFILE VIEWER
class ProfileWindow(QWidget):
    '''
    temp docstring
    '''
    def __init__(self, name: str, admin: bool = False) -> None:
        super().__init__()
        self.admin = admin

        self.profile_manager = PostManager(name, self.admin)
        if not self.profile_manager.loaded:
            self.loaded = False
            return  # handler for if unabe to load profile
        self.loaded = True
        self._draw()

    def _draw(self) -> None:
        self.post_table = QTreeWidget()
        self.post_table.setColumnCount(5)
        self.post_table.setHeaderLabels([TxtPrf.HEADER_POST,
                                         TxtPrf.HEADER_TIME,
                                         TxtPrf.HEADER_EDIT,
                                         TxtPrf.HEADER_PUBLISH,
                                         TxtPrf.HEADER_DELETE])

        usn, pw, bio = self.profile_manager.get_profile_info()
        name_label = QLabel(TxtPrf.LABEL_NAME + usn)
        pw_label = QLabel(TxtPrf.LABEL_PW + pw)
        self.bio_label = QLabel(TxtPrf.LABEL_BIO + bio)

        add_row_button = QPushButton(TxtPrf.BUTTON_CREATE_POST)
        add_row_button.clicked.connect(self._create_post_handler)
        edit_bio_button = QPushButton(TxtPrf.BUTTON_EDIT_BIO)
        edit_bio_button.clicked.connect(self._edit_bio_handler)
        self.pub_bio_button = QPushButton(TxtPrf.BUTTON_PUBLISH_BIO)
        self.pub_bio_button.clicked.connect(self._publish_bio_handler)

        for i, j in self.profile_manager.fetch_posts():
            self.profile_manager.log(f"Added row with content {i}, time {j}",
                                     "profile viewer init")
            self._create_row(i, j)  # i is a tuple with content and time

        layout = QGridLayout(self)
        layout.addWidget(name_label, 0, 0)
        layout.addWidget(pw_label, 0, 1, Qt.AlignCenter)
        layout.addWidget(self.bio_label, 0, 2, Qt.AlignRight)
        layout.addWidget(add_row_button, 1, 0)
        layout.addWidget(self.pub_bio_button, 1, 1)
        layout.addWidget(edit_bio_button, 1, 2)
        layout.addWidget(self.post_table, 2, 0, 1, 4 if self.admin else 3)
        self.setLayout(layout)

    def _create_row(self, content: str, time: str) -> None:
        '''
        Create an additional row containing the post string and timestamp.
        Adds functional buttons to the rows to edit, delete, or publish posts.

        Parameters
        --------
        content : str
            The contents of the post.
        time : str
            The timestamp of the post, as already formatted text.
        '''
        item = QTreeWidgetItem(self.post_table, [content])

        edit_button = QPushButton(TxtPrf.BUTTON_EDIT_POST, self)
        edit_button.clicked.connect(self._generate_button_handler(1, item))

        publish_button = QPushButton(TxtPrf.BUTTON_PUBLISH_POST, self)
        publish_button.clicked.connect(self._generate_button_handler(3, item))

        delete_button = QPushButton(TxtPrf.BUTTON_DELETE_POST, self)
        delete_button.clicked.connect(self._generate_button_handler(2, item))

        items = [QLabel(time), edit_button, publish_button, delete_button]
        for pos, i in enumerate(items):
            self.post_table.setItemWidget(item, pos + 1, i)

    def _login_server(self, pm: PostManager) -> Client:
        if not pm.verify_joinable():
            host = pg().get_host_prompt().get_response()
            if not host:
                return None
            port = pg().get_port_prompt().get_response()
            if not port:
                return None
            pm.log(f"got host:port {host}:{port}", "join button handler")
            if not pm.update_server_info(host, port):
                return None

        server, port, username, password = pm.get_server_info()
        client = Client(server, port)
        if not client.login(username, password):
            pm.update_server_info(reset=True)
            pm.log(f"failed to join server {server}:{port}",
                   "join button handler", True, username, password)
            return None
        return client

    def _create_post_handler(self) -> None:
        content = pg().get_post_prompt().get_response()
        if content:
            self.profile_manager.log(f"attempting to add {content}",
                                     "create post button handler")
            time = self.profile_manager.create_post(content)
            self._create_row(content, time)

    def _edit_bio_handler(self) -> None:
        bio = pg().get_bio_prompt().get_response()
        if bio:
            self.profile_manager.edit_bio(bio)
            self.bio_label.setText("Bio: " + bio)

    def _publish_bio_handler(self) -> bool:
        bio = self.profile_manager.get_profile_info()[2]
        client = self._login_server(self.profile_manager)
        if not client:
            return False
        return client.update_bio(bio)

    def _edit_login_handler(self) -> None:
        username = pg().get_edit_username_prompt().get_response()
        if username:
            self.profile_manager.edit_usn(username)

        password = pg().get_edit_password_prompt().get_response()
        if password:
            self.profile_manager.edit_pw(password)

        self.profile_manager.log("made changes, reload program",
                                 "modify usn/pw button handler")

    def _generate_button_handler(self, version: int,
                                 item: QTreeWidgetItem) -> Callable[..., None]:
        parent = self.post_table
        pm = self.profile_manager

        match version:
            case 1:  # editing a post
                def edit_handler():
                    index = parent.indexOfTopLevelItem(item)
                    post = pm.index_post(index)
                    content = pg().get_edit_post_prompt(post[0]).get_response()
                    if content:
                        pm.edit_post(index, content)
                        parent.setItemWidget(item, 0, QLabel(content))
                return edit_handler
            case 2:  # deleting a post
                def delete_handler():
                    index = parent.indexOfTopLevelItem(item)
                    parent.takeTopLevelItem(index)  # remove at that index
                    pm.del_post(index)
                    self.profile_manager.log(f"successfully post at {index}",
                                             "delete post button handler")
                return delete_handler
            case 3:  # publishing a post
                def publish_handler():  # first fetch mandatory send commands
                    index = parent.indexOfTopLevelItem(item)
                    post = pm.index_post(index)
                    client = self._login_server(pm)
                    if client:
                        client.publish_post(post[0])
                    return publish_handler


class MessengerWindow(QWidget):
    '''
    temp docstring
    '''
    def __init__(self, name: str, admin: bool = False) -> None:
        super().__init__()
        self.admin = admin

        self.message_manager = DmManager(name, self.admin)
        if not self.message_manager.loaded:
            self.loaded = False
            return  # handler for if unabe to load profile
        self.loaded = True
        self._draw()

    def _draw(self) -> None:
        self.friend_table = QTreeWidget()
        self.friend_table.setHeaderHidden(True)

        self.text_editor = QPlainTextEdit()

        send_button = QPushButton(TxtMsg.BUTTON_SEND_MSG)
        send_button.clicked.connect(self._send_handler)

        add_friend_button = QPushButton(TxtMsg.BUTTON_ADD_FRIEND)
        add_friend_button.clicked.connect(self._add_friend_button_handler)

        for i in self.message_manager.fetch_friends():
            self.message_manager.log(f"Added row with content {i.get_name()}",
                                     "messenger init")
            self._add_friend_row(i.get_name())

        self.message_table =QTreeWidget()
        self.message_table.setHeaderHidden(True)

        layout = QGridLayout(self)
        layout.addWidget(self.friend_table, 0, 0, 2, 1)
        layout.addWidget(self.message_table, 0, 1)
        layout.addWidget(self.text_editor, 1, 1)
        layout.addWidget(send_button, 2, 1)
        layout.addWidget(add_friend_button, 2, 0)
        
        self.setLayout(layout)

    def _add_friend_row(self, friend):
        item = QTreeWidgetItem(self.friend_table, [friend])
        self.friend_table.setItemWidget(item, 0, QLabel(friend))

    def _send_handler(self):
        pass

    def _add_friend_button_handler(self):
        '''
        Prompt the user via dialog boxes for a username of a friend.
        '''
        friend = pg().get_friend_prompt().get_response()

        if not friend:
            return
        self._add_friend_row(friend)
        self.message_manager.add_friend(friend)
        return  # Should give feedback to the user if successful or not


def main_gui():
    '''
    Main entry point to program. Automatically starts and opens
    DSU client GUI.
    '''
    app = QApplication([])

    window = ProfileMenu()
    window.resize(MAIN_WIDTH, MAIN_HEIGHT)
    window.setWindowTitle(TxtDsu.WINDOW_MAIN)
    window.show()
    app.exec()
    app.quit()


if __name__ == '__main__':
    print('Welcome to the ICS32 Distributed Social Client! Launching GUI...')
    main_gui()
