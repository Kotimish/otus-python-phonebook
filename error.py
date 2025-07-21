import text


class InvalidPhoneError(ValueError):
    def __init__(self, phone, message=text.incorrect_phone_error):
        self.phone = phone
        self.message = message.format(phone=self.phone)
        super().__init__(self.message)


class InvalidJSONError(ValueError):
    def __init__(self, file_path, message=text.incorrect_json_file_error):
        self.file_path = file_path
        self.message = message.format(file_path=self.file_path)
        super().__init__(self.message)


class InvalidContactIDError(Exception):
    def __init__(self, contact_id, message=text.incorrect_contact_id_error):
        self.contact_id = contact_id
        self.message = message.format(idx=self.contact_id)
        super().__init__(self.message)


class ContactNotFoundError(Exception):
    def __init__(self, contact_id, message=text.not_found_contact_error):
        self.contact_id = contact_id
        self.message = message.format(idx=self.contact_id)
        super().__init__(self.message)
