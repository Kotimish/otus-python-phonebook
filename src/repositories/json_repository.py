import json

from src.interfaces.repository import IRepository


class JsonRepository(IRepository):
    """Класс для работы с файлами (загрузка/сохранение)."""
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> dict:
        """
        Загрузка json-файла
        """
        with open(self.file_path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        return data

    def save(self, data: dict):
        """
        Сохранение json-файла
        """
        with open(self.file_path, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
