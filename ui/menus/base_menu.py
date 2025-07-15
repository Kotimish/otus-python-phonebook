from core import actions
from ui import render, user_input

def missing_menu(context: dict) -> str:
    """Базовое меню для информирования о недоступности запрошенного меню"""
    menu_name = 'Ошибка'
    menu_options = {
        '0': {'label': 'Вернуться в предыдущее меню', 'action': actions.go_back_menu},
    }
    text = 'В системе отсутствует указанное меню'

    render.render_interface(menu_name, extra_info=text)
    # Отрисовка интерфейса
    render.render_choice_interface(menu_options)
    user_choice = user_input.get_user_menu_choice(menu_options)
    if user_choice is None:
        return actions.restart_menu(context)
    return user_choice(context)
