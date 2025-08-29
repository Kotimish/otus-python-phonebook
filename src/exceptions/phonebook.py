from src import text
from src.exceptions.base_exception import BasePhonebookException


class PhonebookException(BasePhonebookException):
    """Базовое исключение для контактов"""


class InvalidContactIDError(PhonebookException):
    def __init__(self, contact_id, message=text.incorrect_contact_id_error):
        """Некорректный ID контакта"""
        self.contact_id = contact_id
        self.message = message.format(idx=self.contact_id)
        super().__init__(self.message)


class ContactNotFoundError(PhonebookException):
    """"""
    def __init__(self, contact_id, message=text.not_found_contact_error):
        self.contact_id = contact_id
        self.message = message.format(idx=self.contact_id)
        super().__init__(self.message)
