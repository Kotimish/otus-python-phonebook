import json


phonebook = {}


def create_contact(contact: dict) -> int:
    """
    Создает контакт на основе введенных данных
    :param contact: Данные нового контакта
    :return: ID нового контакта
    """
    next_id = _next_id()
    phonebook[next_id] = {
        'name': contact[0],
        'phone': contact[1],
        'comment': contact[2],
    }
    return next_id


def _next_id() -> int:
    """
    Отдают следующий свободный id
    :return: Доступный ID
    """
    return max(phonebook, default=0) + 1


def find_contact(word: str) -> dict[int, dict]:
    """
    Поиск контакт(а/ов) по ключевому слову
    :param word: искомое слово
    :return: Словарь из всех найденных контактов
    """
    result_pb = {}
    for idx, contact in phonebook.items():
        for _, entity in contact.items():
            if word.lower() in entity.lower():
                result_pb[idx] = contact
                break
    return result_pb


def get_contact(contact_id: int) -> dict:
    """
    Получение контакта
    :param contact_id: ID искомого контакта
    :return: Контакт в виде словаря
    """
    return phonebook.get(contact_id, {})


def edit_contact(contact_id: int, edited_contact: dict) -> dict:
    """
    Изменить контакт
    :param contact_id: ID изменяемого контакта
    :param edited_contact: Словарь с новыми параметрами для изменения
    :return: Словарь с данными об измененном контакте
    """
    origin_contact = phonebook[contact_id]
    for key in origin_contact:
        new_value = edited_contact.get(key, '')
        if new_value:
            origin_contact[key] = new_value
    return origin_contact


def delete_contact(contact_id: int) -> dict:
    """
    Удалить контакт
    :param contact_id: ID удаляемого контакта
    :return: Словарь с данными об удаленном контакте
    """
    contact = phonebook.pop(contact_id)
    return contact

def load_json(file_path: str) -> dict:
    """
    Загрузка json-файла
    :param file_path: Путь к файлу с телефонным справочником
    :return: Данные о контактах в виде словаря
    """
    # todo убрать при переходе на ООП
    global phonebook
    with open(file_path, 'r', encoding='UTF-8') as file:
        result = json.load(file)
        phonebook = {
            idx: contact
            for idx, contact in enumerate(result.get('phonebook', []), 1)
        }

    return phonebook


def save_json(file_path: str):
    """
    Сохранение json-файла
    :param file_path: Путь к файлу с телефонным справочником
    """
    data = {'phonebook': []}
    contacts = data['phonebook']
    for contact in phonebook.values():
        contacts.append(contact)
    with open(file_path, 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
