# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

# pylint: disable = no-name-in-module

'''
Contains the localizations and prompt generator for GUI.
'''

from PySide6.QtWidgets import QInputDialog
import us_eng

DEFAULT_IP = "168.235.86.101"
DEFAULT_PORT = 3021
TxtDsu = us_eng.DsuEnglish
TxtPrf = us_eng.ProfileEnglish
TxtMsg = us_eng.MsgEnglish
TxtPmt = us_eng.PromptsEnglish


class UserPrompt(QInputDialog):
    """
    Class for user prompt, to check if input is blank or not.
    """
    def __init__(self, window_name: str, prompt_text: str,
                 empty_text: str) -> None:
        super().__init__()
        self.setWindowTitle(window_name)
        self.prompt_text = prompt_text
        self.default_text = ''
        self.empty_text = empty_text

    def get_response(self):
        '''
        Resets labels and loops until user enters valid
        input or quits.
        '''
        self.setLabelText(self.prompt_text)
        self.setTextValue(str(self.default_text))
        while True:
            if self.exec():
                if self._check_valid():
                    return self.textValue()
            else:
                return None

    def append_prompt(self, text: str):
        '''
        Appends text to the prompt
        '''
        self.prompt_text += text

    def set_default_text(self, text: str):
        '''
        Sets the defualt text in the dialog box.
        '''
        self.default_text = text

    def _check_valid(self) -> bool:
        '''
        Returns if the input is valid.
        '''
        if self._check_blanks():
            self.setLabelText(self.empty_text)
            return False
        return True

    def _check_blanks(self) -> bool:
        '''
        Returns if the input is not whitespace or empty.
        '''
        return not self.textValue() or self.textValue().isspace()


class UniquePrompt(UserPrompt):
    '''
    Child of prompt, now enforces uniqueness.
    '''
    def __init__(self, window_name: str, prompt_text: str,
                 empty_text: str, dupe_text: str) -> None:
        super().__init__(window_name, prompt_text, empty_text)
        self.dupe_text = dupe_text
        self.dupe_list = tuple()

    def set_duplicate_list(self, lst: tuple) -> None:
        '''
        Sets the list to check for duplicates of.
        '''
        self.dupe_list = lst

    def _check_valid(self) -> bool:
        '''
        Checks for blanks and duplicates. If neither, returns true.
        '''
        if not super()._check_valid():
            return False
        if self._check_duplicate():
            self.setLabelText(self.dupe_text)
            return False
        return True

    def _check_duplicate(self) -> bool:
        '''
        Returns if inputted value is not duplicate
        '''
        return self.textValue() in self.dupe_list


class PromptGenerator:
    '''
    Class to return prompts.
    '''
    def __init__(self) -> None:
        pass

    def get_username_prompt(self, other_usernames):
        '''
        Prompt for getting username in profile creation.
        '''
        prompt = UniquePrompt(TxtPmt.POPUP_HEADER_CREATE_PROFILE,
                              TxtPmt.POPUP_PROMPT_GET_NAME,
                              TxtPmt.POPUP_PROMPT_GET_NAME_BLANK,
                              TxtPmt.POPUP_PROMPT_GET_NAME_DUPLICATE)
        prompt.set_duplicate_list(other_usernames)
        return prompt

    def get_password_prompt(self):
        '''
        Prompt for getting password in profile creation.
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_CREATE_PROFILE,
                            TxtPmt.POPUP_PROMPT_GET_PW,
                            TxtPmt.POPUP_PROMPT_GET_PW_BLANK)
        return prompt

    def get_post_prompt(self):
        '''
        Prompt for getting post content in post creation.
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_CREATE_POST,
                            TxtPmt.POPUP_PROMPT_GET_CONTENT,
                            TxtPmt.POPUP_PROMPT_GET_CONTENT_BLANK)
        return prompt

    def get_bio_prompt(self):
        '''
        Prompt for getting bio in bio editing.
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_EDIT_BIO,
                            TxtPmt.POPUP_PROMPT_GET_BIO,
                            TxtPmt.POPUP_PROMPT_GET_BIO_BLANK)
        return prompt

    def get_edit_username_prompt(self):
        '''
        Prompt for getting username in editing login.
        Intended only for admin. Deprecated.
        '''
        prompt = UserPrompt("ADMIN: ENTER USERNAME",
                            "ENTER USERNAME",
                            "USERNAME CANNOT BE BLANK")
        return prompt

    def get_edit_password_prompt(self):
        '''
        Prompt for getting password in editing login.
        Intended only for admin. Deprecated.
        '''
        prompt = UserPrompt("ADMIN: ENTER PASSWORD",
                            "ENTER PASSWORD",
                            "PASSWORD CANNOT BE BLANK")
        return prompt

    def get_edit_post_prompt(self, past_post):
        '''
        Prompt for getting new post content in post editing.
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_EDIT_POST,
                            TxtPmt.POPUP_PROMPT_GET_EDIT + past_post,
                            TxtPmt.POPUP_PROMPT_GET_EDIT_BLANK)
        prompt.set_default_text(past_post)
        return prompt

    def get_host_prompt(self):
        '''
        Prompt for getting host IP when joining server.
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_SERVER,
                            TxtPmt.POPUP_PROMPT_GET_IP + DEFAULT_IP,
                            TxtPmt.POPUP_PROMPT_GET_IP_BLANK)
        prompt.set_default_text(DEFAULT_IP)
        return prompt

    def get_port_prompt(self):
        '''
        Prompt for getting host port when joining server.
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_SERVER,
                            TxtPmt.POPUP_PROMPT_GET_PORT +
                            str(DEFAULT_PORT),
                            TxtPmt.POPUP_PROMPT_GET_PORT_BLANK)
        prompt.set_default_text(DEFAULT_PORT)
        return prompt

    def get_friend_prompt(self, lst: list):
        '''
        Prompt for getting friend when adding friend.
        '''
        prompt = UniquePrompt(TxtPmt.POPUP_HEADER_ADD_FRIEND,
                              TxtPmt.POPUP_PROMPT_GET_FRIEND,
                              TxtPmt.POPUP_PROMPT_GET_FRIEND_BLANK,
                              TxtPmt.POPUP_PROMPT_GET_FRIEND_SELF)
        prompt.set_duplicate_list(lst)
        return prompt
