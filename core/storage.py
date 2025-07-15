import json


def load_json(file_path: str) -> dict:
    """
    Загрузка json-файла
    """
    with open(file_path, 'r', encoding='UTF-8') as file:
        result = json.load(file)

    return result


def save_json(file_path: str, data: dict):
    """
    Сохранение json-файла
    """
    with open(file_path, 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
