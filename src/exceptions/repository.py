from src import text
from src.exceptions.base_exception import BasePhonebookException

class RepositoryException(BasePhonebookException):
    """Базовое исключение для репозитория"""

class RepositoryPathError(RepositoryException):
    def __init__(self, file_path, message=text.not_found_file_error):
        """Некорректный путь до файла"""
        self.file_path = file_path
        self.message = message.format(file_path=self.file_path)
        super().__init__(self.message)


class IncorrectRepositoryDataError(RepositoryException):
    def __init__(self, file_path, message=text.incorrect_file_data_error):
        """Некорректный тип данных файла"""
        self.file_path = file_path
        self.message = message.format(file_path=self.file_path)
        super().__init__(self.message)
