import os
import text
from model.contact import Contact


def show_message(message: str):
    """
    Отображает переданное сообщение пользователю
    :param message: Текст сообщения
    """
    print(message)


def show_menu(title: str, options: list):
    """
    Отрисовывает меню
    :param title: Название меню
    :param options: Доступные опции
    """
    print(title)
    for number, item in enumerate(options):
        print(f'\t{number + 1}. {item}')


def show_contacts(phonebook: dict[int, Contact], error_message: str):
    """
    Отображает переданные контакты
    :param phonebook: Список контактов для показа в виде словаря
    :param error_message: Сообщение об ошибки в случае пустого словаря
    """
    if not phonebook:
        show_message(error_message)
        return
    for idx, contact in phonebook.items():
        show_message(text.show_contact.format(idx=idx, contact=str(contact)))


def get_user_menu_choice(menu_options: list):
    """
    Получение и обработка выбора пункта меню от пользователя
    :param menu_options: меню с возможными пунктами выбора
    :return: возвращает соответствующее действие для выбранного пункта меню
    """
    while True:
        user_choice = input_date(text.user_menu_choice).strip()
        if (
                user_choice.isdigit() and
                0 < int(user_choice) <= len(menu_options)
        ):
            return int(user_choice)
        print(text.user_menu_choice_error.format(menu_options=len(menu_options)))


def input_date(message: str|list[str]) -> str|list[str]:
    """
    Получает от пользователя ввод данных
    :param message: Сообщение для пользователя с запросом данных
    :return: строку или список из строк с ответом пользователя
    """
    if isinstance(message, str):
        message = [message]
    result = []
    for msg in message:
        # todo продумать корректный ввод при ошибки
        try:
            result.append(input(msg))
        except UnicodeDecodeError:
            show_message(text.decode_error)
    return result if len(result) > 1 else result[0]


def clear_terminal():
    """Очистка терминала"""
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    else:
        print('Ошибка при очистке экрана, неопределенный тип операционной системы')
