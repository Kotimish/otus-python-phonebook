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


class LoadingRepositoryDataError(RepositoryException):
    def __init__(self, file_path, message=text.incorrect_loading_file_data_error):
        """Некорректная загрузка данных из  файла"""
        self.file_path = file_path
        self.message = message.format(file_path=self.file_path)
        super().__init__(self.message)


class SavingRepositoryDataError(RepositoryException):
    """"""
    def __init__(self, data, message=text.incorrect_saving_file_data_error):
        """Некорректное сохранение данных в файл"""
        self.data = data
        self.message = message.format(data=self.data)
        super().__init__(self.message)
