from core import actions
from ui import render, user_input


def contact_search_menu(context: dict) -> str:
    """Меню поиска контакта"""
    menu_name = 'Меню поиска'
    menu_options = {
        '1': {'label': 'Поиск контакта по id', 'action': actions.get_contact_by_id},
        '2': {'label': 'Поиск по имени', 'action': actions.get_contact_by_name},
        '3': {'label': 'Поиск по номеру', 'action': actions.get_contact_by_number},
        '0': {'label': 'Вернуться в предыдущее меню', 'action': actions.go_back_menu},
    }
    render.render_interface(menu_name)
    render.render_choice_interface(menu_options)
    user_choice = user_input.get_user_menu_choice(menu_options)
    if user_choice is None:
        return actions.go_back_menu(context)
    return user_choice(context)
