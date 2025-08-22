from src import text
from src.exceptions.base_exception import BasePhonebookException


class ContactException(BasePhonebookException):
    """Базовое исключение для контактов"""


class InvalidPhoneNumberError(ContactException):
    def __init__(self, phone, message=text.incorrect_phone_error):
        self.phone = phone
        self.message = message.format(phone=self.phone)
        super().__init__(self.message)


class InvalidContactNameError(ContactException):
    def __init__(self, name, message=text.incorrect_contact_name_error):
        self.name = name
        self.message = message.format(name=self.name)
        super().__init__(self.message)
