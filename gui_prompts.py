# JONATHAN PATRICK CHEN
# JONATPC2@UCI.EDU
# 80752008

# pylint: disable = no-name-in-module

'''
Temp docstring
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
    Temp docstring
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
        temp docstring
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
        temp docstring
        '''
        self.prompt_text += text

    def set_default_text(self, text: str):
        '''
        temp docstring
        '''
        self.default_text = text

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
                 empty_text: str, dupe_text: str) -> None:
        super().__init__(window_name, prompt_text, empty_text)
        self.dupe_text = dupe_text
        self.dupe_list = tuple()

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
        prompt = UniquePrompt(TxtPmt.POPUP_HEADER_CREATE_PROFILE,
                              TxtPmt.POPUP_PROMPT_GET_NAME,
                              TxtPmt.POPUP_PROMPT_GET_NAME_BLANK,
                              TxtPmt.POPUP_PROMPT_GET_NAME_DUPLICATE)
        prompt.set_duplicate_list(other_usernames)
        return prompt


    def get_password_prompt(self):
        '''
        temp docstring
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_CREATE_PROFILE,
                            TxtPmt.POPUP_PROMPT_GET_PW,
                            TxtPmt.POPUP_PROMPT_GET_PW_BLANK)
        return prompt


    def get_post_prompt(self):
        '''
        temp docstring
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_CREATE_POST,
                            TxtPmt.POPUP_PROMPT_GET_CONTENT,
                            TxtPmt.POPUP_PROMPT_GET_CONTENT_BLANK)
        return prompt


    def get_bio_prompt(self):
        '''
        temp docstring
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_EDIT_BIO,
                            TxtPmt.POPUP_PROMPT_GET_BIO,
                            TxtPmt.POPUP_PROMPT_GET_BIO_BLANK)
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
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_EDIT_POST,
                            TxtPmt.POPUP_PROMPT_GET_EDIT + past_post,
                            TxtPmt.POPUP_PROMPT_GET_EDIT_BLANK)
        prompt.set_default_text(past_post)
        return prompt

    def get_host_prompt(self):
        '''
        temp docstring
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_SERVER,
                            TxtPmt.POPUP_PROMPT_GET_IP + DEFAULT_IP,
                            TxtPmt.POPUP_PROMPT_GET_IP_BLANK)
        prompt.set_default_text(DEFAULT_IP)
        return prompt

    def get_port_prompt(self):
        '''
        temp docstring
        '''
        prompt = UserPrompt(TxtPmt.POPUP_HEADER_SERVER,
                            TxtPmt.POPUP_PROMPT_GET_PORT +
                            str(DEFAULT_PORT),
                            TxtPmt.POPUP_PROMPT_GET_PORT_BLANK)
        prompt.set_default_text(DEFAULT_PORT)
        return prompt
