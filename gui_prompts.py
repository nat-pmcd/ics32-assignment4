# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

# pylint: disable = no-name-in-module

'''
Temp docstring
'''

from PySide6.QtWidgets import QInputDialog
from us_eng import (POPUP_HEADER_CREATE_PROFILE,  # pylint does not like
                    POPUP_PROMPT_GET_NAME,        # wildcard import...
                    POPUP_PROMPT_GET_NAME_BLANK,
                    POPUP_PROMPT_GET_NAME_DUPLICATE,
                    POPUP_PROMPT_GET_PW,
                    POPUP_PROMPT_GET_PW_BLANK,
                    POPUP_HEADER_CREATE_POST,
                    POPUP_PROMPT_GET_CONTENT,
                    POPUP_PROMPT_GET_CONTENT_BLANK,
                    POPUP_HEADER_EDIT_BIO,
                    POPUP_PROMPT_GET_BIO,
                    POPUP_PROMPT_GET_BIO_BLANK,
                    POPUP_HEADER_EDIT_POST,
                    POPUP_PROMPT_GET_EDIT,
                    POPUP_PROMPT_GET_EDIT_BLANK)

class UserPrompt(QInputDialog):
    """
    Temp docstring
    """
    def __init__(self, window_name: str, prompt_text: str,
                 empty_text: str) -> None:
        super().__init__()
        self.setWindowTitle(window_name)
        self.prompt_text = prompt_text
        self.empty_text = empty_text

    def get_response(self):
        '''
        temp docstring
        '''
        self.setLabelText(self.prompt_text)
        while True:
            if self.exec():
                if self._check_valid():
                    return self.textValue()
            else:
                return None

    def append_prompt(self, text: str):
        '''
        temp docstring
        '''
        self.prompt_text += text

    def _check_valid(self):
        if self._check_blanks():
            self.setLabelText(self.empty_text)
            return False
        return True

    def _check_blanks(self) -> bool:
        return not self.textValue() or self.textValue().isspace()


class UniquePrompt(UserPrompt):
    '''
    Temp docstring
    '''
    def __init__(self, window_name: str, prompt_text: str,
                 empty_text: str, dupe_text: str, lst: tuple = None) -> None:
        super().__init__(window_name, prompt_text, empty_text)
        self.dupe_text = dupe_text
        self.dupe_list = [].copy() if lst is not None else lst

    def set_duplicate_list(self, lst: tuple) -> None:
        '''
        temp docstring
        '''
        self.dupe_list = lst

    def _check_valid(self):
        if not super()._check_valid():
            return False
        if self._check_duplicate():
            self.setLabelText(self.dupe_text)
            return False
        return True

    def _check_duplicate(self) -> bool:
        return self.textValue() in self.dupe_list


class PromptGenerator:
    '''
    temp docstring
    '''
    def __init__(self) -> None:
        pass

    def get_username_prompt(self, other_usernames):
        '''
        temp docstring
        '''
        prompt = UniquePrompt(POPUP_HEADER_CREATE_PROFILE,
                              POPUP_PROMPT_GET_NAME,
                              POPUP_PROMPT_GET_NAME_BLANK,
                              POPUP_PROMPT_GET_NAME_DUPLICATE,
                              other_usernames)
        return prompt


    def get_password_prompt(self):
        '''
        temp docstring
        '''
        prompt = UserPrompt(POPUP_HEADER_CREATE_PROFILE,
                            POPUP_PROMPT_GET_PW,
                            POPUP_PROMPT_GET_PW_BLANK)
        return prompt


    def get_post_prompt(self):
        '''
        temp docstring
        '''
        prompt = UserPrompt(POPUP_HEADER_CREATE_POST,
                            POPUP_PROMPT_GET_CONTENT,
                            POPUP_PROMPT_GET_CONTENT_BLANK)
        return prompt


    def get_bio_prompt(self):
        '''
        temp docstring
        '''
        prompt = UserPrompt(POPUP_HEADER_EDIT_BIO,
                            POPUP_PROMPT_GET_BIO,
                            POPUP_PROMPT_GET_BIO_BLANK)
        return prompt


    def get_edit_username_prompt(self):
        '''
        temp docstring
        '''
        prompt = UserPrompt("ADMIN: ENTER USERNAME",
                            "ENTER USERNAME",
                            "USERNAME CANNOT BE BLANK")
        return prompt


    def get_edit_password_prompt(self):
        '''
        temp docstring
        '''
        prompt = UserPrompt("ADMIN: ENTER PASSWORD",
                            "ENTER PASSWORD",
                            "PASSWORD CANNOT BE BLANK")
        return prompt


    def get_edit_post_prompt(self, past_post):
        '''
        temp docstring
        '''
        prompt = UserPrompt(POPUP_HEADER_EDIT_POST,
                            POPUP_PROMPT_GET_EDIT + past_post,
                            POPUP_PROMPT_GET_EDIT_BLANK)
        return prompt
