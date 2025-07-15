import re
from pathlib import Path


def is_phone_number(number: str) -> bool:
    """
    Проверка строки на принадлежность к телефонному номеру.
    Телефонный номер должен иметь спец символ + в начале,
    должен быть длинной от 7 до 15 символов, включая код страны
    и может иметь спец символы (Скобки, пробельные символы, дефисы и тире)
    :param number: Проверяемая строка с телефонным номером
    :return: True, если строка является телефонным номером, иначе False
    """
    # Список разрешенных спец-символов в телефонном номере
    # Скобки, пробельные символы, дефисы и тире
    pattern = r'[\(\)\s\u002D\u2010\u2011\u2012\u2013\u2014\u2212]+'
    if not number:
        print('Ошибка. Отсутствует номер')
        return False
    if len(number) > 0 and number[0] != '+':
        print('Ошибка. Пропущен указатель на международный код страны')
        return False
    number = number[1:]
    number = re.sub(pattern, '', number)
    if not number.isdigit():
        print('Ошибка. В номере присутствуют недопустимые символы')
        return False
    if not (7 < len(number) < 15):
        print('Ошибка. Некорректная длина телефонного номера')
        return False
    return True

def is_valid_new_file_path(path_str: str) -> bool:
    """
    Проверка пути к новому файлу на валидность
    :param path_str: Проверяемый путь до файла
    :return: True, если путь корректный, иначе False
    """
    allowed_file_types = ['json',]
    if not path_str:
        return False
    path = Path(path_str)
    # Проверяем название и тип файла
    if not (
        path.stem and
        path.suffix in allowed_file_types
    ):
        return False

    if not path.exists():
        # Проверка нового файла по родительскому элементу
        parent = path.parent
        return (
            parent and
            parent.exists() and
            parent.is_dir()
        )
    elif path.is_file():
        return True
    return False

def is_valid_file_path(path_str: str) -> bool:
    """
    Проверка пути к файлу на валидность
    :param path_str: Проверяемый путь до файла
    :return: True, если путь корректный, иначе False
    """
    if not path_str:
        return False
    path = Path(path_str)

    return (
        path.exists() and
        path.is_file()
    )

def is_valid_phonebook(phonebook: list) -> bool:
    pass
