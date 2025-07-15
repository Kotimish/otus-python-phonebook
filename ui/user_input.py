from settings import MAX_USER_INPUT_ATTEMPTS
from ui import render


def ask_yes_no(question: str, default: str = "yes"):
    """
    Создание и получения ответа пользователя на закрытый вопрос
    :param question: текст закрытого вопроса
    :param default: ответ по умолчанию
    :return: возвращает True для положительного ответа и False для отрицательного
    """
    valid_input = {
        "yes": True, "y": True, "no": False, "n": False,
        "да": True, "д": True, "нет": False, "н": False,
    }
    error_message = ''
    attempt_count = 0
    while attempt_count < MAX_USER_INPUT_ATTEMPTS:
        render.clear_terminal()
        if error_message:
            print(error_message)
        user_input = input(f"{question} (y/n): ").strip().lower()
        if not user_input:
            user_input = default
        if user_input in valid_input:
            return valid_input[user_input]
        error_message = "Ошибка: введите 'y' или 'n'"
        attempt_count += 1
    print(f'Превышено число попыток ввода. Будет использовано дефолтное значение: {default}')
    input('Нажмите Enter чтобы продолжить...')
    return None


def get_user_menu_choice(menu_options: dict):
    """
    Получение и обработка выбора пункта меню от пользователя
    :param menu_options: меню с возможными пунктами выбора
    :return: возвращает соответствующее действие для выбранного пункта меню
    """
    attempt_count = 0
    while attempt_count < MAX_USER_INPUT_ATTEMPTS:
        user_choice = input('Выберите пункт меню: ').strip()
        if user_choice in menu_options:
            return menu_options[user_choice]['action']
        print(f'Некорректный ввод. Допустимые варианты: {", ".join(menu_options.keys())}')
        attempt_count += 1
    print('Превышено число попыток ввода. Возврат в предыдущее меню')
    input('Нажмите Enter чтобы продолжить...')
    return None
