from core import actions
from ui import render, user_input


def default_menu(context: dict) -> str:
    """Функция-заглушка для примера работы функции отрисовки интерфейса"""
    menu_name = 'Добро пожаловать'
    menu_options = {
        '0': {'label': 'Выход', 'action': actions.close_phonebook},
    }
    render.render_interface(menu_name, )
    render.render_choice_interface(menu_options)
    action = user_input.get_user_menu_choice(menu_options)
    if action is None:
        return actions.go_back_menu(context)
    return action(context)
