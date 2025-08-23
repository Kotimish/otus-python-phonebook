import json

from src.interfaces.repository import IRepository
import src.exceptions.repository as exceptions


class JsonRepository(IRepository):
    """Класс для работы с файлами (загрузка/сохранение)."""
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> dict:
        """
        Загрузка json-файла
        """
        try:
            with open(self.file_path, 'r', encoding='UTF-8') as file:
                data = json.load(file)
        except FileNotFoundError as e:
            raise exceptions.RepositoryPathError(file_path=self.file_path)
        except json.JSONDecodeError as e:
            raise exceptions.IncorrectRepositoryDataError(file_path=self.file_path)
        return data

    def save(self, data: dict):
        """
        Сохранение json-файла
        """
        with open(self.file_path, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
