import utils
from core import storage, validation
from settings import MAX_USER_INPUT_ATTEMPTS, MAX_SHOW_CONTACTS
from ui import user_input


def open_phonebook(context: dict) -> str:
    """
    Открытие телефонного справочника
    :param context: Контекст
    :return: Статус перехода в основное меню приложения
    """
    if 'file' not in context:
        print('Ошибка. Отсутствует информация о файле с контактами')
        return go_back_menu(context)
    if not validation.is_valid_file_path(context['file']):
        print('Ошибка. По указанному пути не существует файла')
        return restart_menu(context)

    data = storage.load_json(context['file'])
    context['phonebook'] = data['phonebook']
    context['max_id'] = utils.get_max_id(data['phonebook'])
    return 'main_menu'

def change_phonebook(context):
    """
    Изменение пути к файлу телефонного справочника
    :param context: Контекст
    :return: Статус перехода в приветственное меню приложения
    """
    # todo продумать более строгие проверки
    attempt_count = 0
    while attempt_count < MAX_USER_INPUT_ATTEMPTS:
        file_path = input('Введите путь к файлу телефонного справочника: ')
        if validation.is_valid_file_path(file_path):
            break
        print(
            'Ошибка. Некорректный ввод.'
        )
        attempt_count += 1
    else:
        print('Превышено число попыток ввода. Возврат в предыдущее меню')
        input('Нажмите Enter чтобы продолжить...')
        return 'welcome_menu'

    context['file'] = file_path
    return 'welcome_menu'

def change_contact_name(context: dict) -> str:
    """
    Изменение названия контакта
    :param context: Контекст
    :return: Статус возврата в текущее меню
    """
    name = input('Введите новое название контакта: ').strip()
    context['current_contact']['name'] = name
    context['is_modified'] = True
    return restart_menu(context)

def change_contact_phone(context: dict) -> str:
    """
    Изменение номера телефону контакта
    :param context: Контекст
    :return: Статус возврата в текущее меню
    """
    attempt_count = 0
    while attempt_count < MAX_USER_INPUT_ATTEMPTS:
        phone_number = input('Введите новый телефон: ')
        if validation.is_phone_number(phone_number):
            break
        print(
            'Ошибка. Некорректный ввод.\n'
            'Телефонный номер должен состоять из кода страны, '
            'чисел и допустимых спец символов.'
        )
        attempt_count += 1
    else:
        print('Превышено число попыток ввода. Возврат в предыдущее меню')
        input('Нажмите Enter чтобы продолжить...')
        return restart_menu(context)
    context['current_contact']['phone'] = phone_number
    context['is_modified'] = True
    return restart_menu(context)

def change_contact_comment(context: dict) -> str:
    """
    Изменение комментария к контакту
    :param context: Контекст
    :return: Статус с возвратом в текущее меню
    """
    comment = input('Введите новый комментарий: ').strip()
    context['current_contact']['comment'] = comment
    context['is_modified'] = True
    return restart_menu(context)

def show_all_contacts(context: dict) -> str:
    """
    Функция выгрузки для показа всех контактов
    :param context: Контекст
    :return: Статус с указанием на меню показа нескольких контактов
    """
    # Обнуляем старые записи во временном блоке
    context['current_contacts'] = []
    phonebook = context.get('phonebook', [])
    if not phonebook:
        print('')
        return 'contacts_menu'
    if not isinstance(phonebook, list):
        print('')
        return 'contacts_menu'

    if len(phonebook) > MAX_SHOW_CONTACTS:
        print(f'Предупреждение. В справочнике больше {MAX_SHOW_CONTACTS}.')
        user_choice = user_input.ask_yes_no('Отобразить все контакты?')
        context['current_contacts'] = phonebook if user_choice else phonebook[:MAX_SHOW_CONTACTS]
    else:
        context['current_contacts'] = phonebook

    return 'contacts_menu'

def show_contact(contact: dict) -> str:
    """
    Шаблон для отображения контакта
    :param contact: Контакт в виде словаря
    :return: Строка с основной информацией о контакте
    """
    for key in ('id', 'name', 'phone'):
        if key not in contact:
            print(f'Ошибка. В контакте отсутствует обязательное поле {key}')
            return ''

    text = (
        f'ID: {contact["id"]}, '
        f'Имя: {contact["name"]}, '
        f'Телефон: {contact["phone"]}'
    )
    if (
        'comment' in contact and
        contact['comment']
    ):
        text += f', Коммент: {contact["comment"]};'
    return text

def create_contact(context: dict) -> str:
    """
    Создание контакта.
    Обязательные поля телефон и название контакта
    :param context: Контекст
    :return: Статус следующего вызываемого меню
    """
    max_id = context.get('max_id', -1)

    attempt_count = 0
    while attempt_count < MAX_USER_INPUT_ATTEMPTS:
        phone_number = input('Введите новый телефон: ').strip()
        if validation.is_phone_number(phone_number):
            break
        print(
            'Ошибка. Некорректный ввод.\n'
            'Телефонный номер должен состоять из кода страны, '
            'чисел и допустимых спец символов.'
        )
        attempt_count += 1
    else:
        print('Превышено число попыток ввода. Возврат в предыдущее меню')
        input('Нажмите Enter чтобы продолжить...')
        return restart_menu(context)

    attempt_count = 0
    while attempt_count < MAX_USER_INPUT_ATTEMPTS:
        name = input('Введите название контакта: ').strip()
        if name:
            break
        print(
            'Ошибка. Название контакта обязательно для ввода.'
        )
        attempt_count += 1
    else:
        print('Превышено число попыток ввода. Возврат в предыдущее меню')
        input('Нажмите Enter чтобы продолжить...')
        return restart_menu(context)

    comment = input('По необходимости введите комментарий к контакту:').strip()
    new_contact = {
        "id": max_id + 1,
        "name": name,
        "phone": phone_number,
        "comment": comment
    }
    # Добавляем в общий список контактов
    if (
        'phonebook' not in context or
        not isinstance(context['phonebook'], list)
    ):
        print('Ошибка. Не удалось зарегистрировать новый контакт')
        return restart_menu(context)
    context['phonebook'].append(new_contact)
    context['current_contact'] = new_contact
    context['is_modified'] = True

    print('Контакт успешно создан')
    input('Нажмите Enter чтобы продолжить...')
    return 'contact_menu'

def get_contact_by_id(context: dict) -> str:
    """
    Поиск/получение контакта по его id.
    Предполагается выдача только одного контакта из-за уникальности id
    :param context: Контекст
    :return: Статус следующего вызываемого меню
    """
    context['current_contact'] = {}

    attempt_count = 0
    while attempt_count < MAX_USER_INPUT_ATTEMPTS:
        contact_id = input('Введите ID искомого контакта: ')
        if contact_id.isdigit():
            break
        print('Некорректный ввод. ID должен быть числом.')
        attempt_count += 1
    else:
        print('Превышено число попыток ввода. Возврат в предыдущее меню')
        input('Нажмите Enter чтобы продолжить...')
        return restart_menu(context)

    contact = search_contact_by_id(context["phonebook"], contact_id)
    if contact is None:
        print('Ошибка. Контакт не найден.')
        input('Нажмите Enter чтобы продолжить...')
        return restart_menu(context)

    # Добавляем найденный контакт в контекст для следующего меню
    context['current_contact'] = contact
    return 'contact_menu'

def search_contact_by_id(contacts, contact_id):
    """
    Поиск/получение контакта по его id.
    Предполагается выдача только одного контакта из-за уникальности id
    :param contacts: Список словарей из контактов
    :param contact_id: уникальный id контакта
    :return: возвращает информацию о контакте в формате словаря
    """
    for contact in contacts:
        if contact_id == contact.get('id'):
            return contact
    return None

def get_contact_by_name(context: dict) -> str:
    """
    Поиск/получение контакта по имени.
    Предполагается выдача нескольких контактов
    :param context: Контекст
    :return: Статус следующего вызываемого меню
    """
    # Явно очищаем
    context['current_contacts'] = []

    name = input('Введите искомое значение: ')
    found_contacts = search_contact_by_field(context['phonebook'], 'name', name)
    if found_contacts:
        context['current_contacts'] = found_contacts
        return 'contacts_menu'
    else:
        print('Ошибка. Контакт не найден.')
        input('Нажмите Enter чтобы продолжить...')
        return restart_menu(context)

def get_contact_by_number(context: dict) -> str:
    """
    Поиск/получение контакта по номеру.
    Предполагается выдача нескольких контактов
    :param context: Контекст
    :return: Статус следующего вызываемого меню
    """
    # Явно очищаем
    context['current_contacts'] = []

    attempt_count = 0
    while attempt_count < MAX_USER_INPUT_ATTEMPTS:
        phone_number = input('Введите номер искомого контакта: ')
        if validation.is_phone_number(phone_number):
            break
        attempt_count += 1
    else:
        print('Превышено число попыток ввода. Возврат в предыдущее меню')
        input('Нажмите Enter чтобы продолжить...')
        return restart_menu(context)

    found_contacts = search_contact_by_field(context['phonebook'], 'phone', phone_number)
    if found_contacts:
        context['current_contacts'] = found_contacts
        return 'contacts_menu'
    else:
        print('Ошибка. Контакт не найден.')
        input('Нажмите Enter чтобы продолжить...')
        return restart_menu(context)

def search_contact_by_field(contacts, field, value):
    """
    Поиск/получение контакта по его id.
    Предполагается выдача списка контактов
    :param contacts: Список словарей из контактов
    :param field: Тип поля, по котору идет поиск
    :param value: значение искомого поля
    :return: возвращает информацию о контакте в формате словаря
    """
    found_contacts = []
    for contact in contacts:
        if contact.get(field) == value:
            found_contacts.append(contact)
    return found_contacts

def delete_contact(context: dict) -> str:
    """
    Удаление контакта.
    Текущая логика ищет позицию контакта по id и удаляет по позиции
    :param context: Контекст
    :return: Статус следующего вызываемого меню
    """
    user_choice = user_input.ask_yes_no('Вы уверено, что хотите удалить контакт?')
    if not user_choice:
        return restart_menu(context)
    if 'current_contact' not in context:
        print('Ошибка. Контакт для удаления не найден.')
    # todo подумать над иным способом удаления
    contacts = context.get('phonebook', [])
    deleted_contact = context['current_contact']
    for position, contact in enumerate(contacts):
        if deleted_contact['id'] == contact['id']:
            break
    else:
        print(f'Ошибка. Контакт с id {deleted_contact["id"]} не был найден')
        input('Нажмите Enter чтобы продолжить...')
        return go_back_menu(context)

    context['is_modified'] = True
    context['phonebook'].pop(position)
    return go_back_menu(context)

def save_phonebook(context: dict) -> str:
    """
    Сохранение изменений телефонного справочника.
    Сброс указателя на изменения в файле.
    :param context: Контекст
    :return: Статус следующего вызываемого меню
    """
    if 'phonebook' not in context:
        print('Ошибка. При сохранении не был найден справочник')
        return restart_menu(context)
    data = {'phonebook': context['phonebook']}
    if 'file' not in context:
        print('Ошибка. Не найден путь сохранения')
    storage.save_json(context['file'], data)
    context['is_modified'] = False
    return restart_menu(context)

def save_phonebook_in_another_file(context: dict) -> str:
    """
    Сохранение изменений телефонного справочника в другой файл.
    Сброс указателя на изменения в файле.
    :param context: Контекст
    :return: Статус следующего вызываемого меню
    """
    change_phonebook(context)
    save_phonebook(context)
    return restart_menu(context)

def close_phonebook(context: dict) -> str:
    """
    Завершение работы с текущим телефонным справочником
    :param context: Контекст
    :return: Статус следующего вызываемого меню
    """
    if (
        context['is_modified'] and
        user_input.ask_yes_no('Сохранить изменения перед выходом?')
    ):
        save_phonebook(context)
    return 'welcome_menu'

def close_app(context: dict) -> str:
    """
    Возврат сигнала на завершение работы с программой
    :param context: Контекст
    :return: Статус закрытия
    """
    return 'exit'

def go_back_menu(context: dict) -> str:
    """
    Возвращает специальный флаг возврата в предыдущее меню
    :param context: Контекст
    :return: Статус предыдущего меню
    """
    return 'back_menu'

def restart_menu(context: dict) -> str:
    """
    Возвращает специальный флаг перезапуска текущего меню
    :param context: Контекст
    :return: Статус текущего меню
    """
    return 'current_menu'
