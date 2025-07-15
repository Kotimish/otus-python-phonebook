from core import actions
from ui import render, user_input


def change_contact_menu(context: dict) -> str:
    menu_name = 'Изменение контакта'
    menu_options = {
        '1': {'label': 'Изменить имя контакта', 'action': actions.change_contact_name},
        '2': {'label': 'Изменить телефон', 'action': actions.change_contact_phone},
        '3': {'label': 'Изменить комментарий', 'action': actions.change_contact_comment},
        '0': {'label': 'Вернуться в предыдущее меню', 'action': actions.go_back_menu},
    }
    contact = context['current_contact']
    if contact:
        text = actions.show_contact(contact)
    else:
        text = 'Ошибка. Отсутствует информация о контакте'

    render.render_interface(menu_name, extra_info=text)
    render.render_choice_interface(menu_options)
    user_choice = user_input.get_user_menu_choice(menu_options)
    if user_choice is None:
        return actions.restart_menu(context)
    return user_choice(context)


def contact_menu(context: dict) -> str:
    """Меню показа контакта"""
    menu_name = 'Контакт'
    menu_options = {
        '1': {'label': 'Изменить контакт', 'action': lambda _: 'change_contact_menu'},
        '2': {'label': 'Удалить контакт', 'action': actions.delete_contact},
        '0': {'label': 'Вернуться в предыдущее меню', 'action': actions.go_back_menu},
    }
    contact = context['current_contact']
    if contact:
        text = actions.show_contact(contact)
    else:
        text = 'Ошибка. Отсутствует информация о контакте'

    render.render_interface(menu_name, extra_info=text)
    # Отрисовка интерфейса
    render.render_choice_interface(menu_options)
    user_choice = user_input.get_user_menu_choice(menu_options)
    if user_choice is None:
        return actions.restart_menu(context)
    return user_choice(context)


def contacts_menu(context: dict) -> str:
    """Меню работы с выбранными контактами"""
    if not context.get('phonebook'):
        print("Ошибка: телефонная книга не загружена")
        return actions.go_back_menu(context)

    menu_name = 'Контакты'
    menu_options = {
        '1': {'label': 'Открыть контакт по ID', 'action': actions.get_contact_by_id},
        '0': {'label': 'Вернуться в предыдущее меню', 'action': actions.go_back_menu},
    }
    text = f'Найдено {len(context["phonebook"])} контакт(а/ов)'
    render.render_interface(menu_name, extra_info=text)
    for contact in context['phonebook']:
        print(f'ID: {contact["id"]}, Имя: {contact["name"]}, Телефон: {contact["phone"]}, Коммент: {contact["comment"]};')
    render.render_choice_interface(menu_options)
    user_choice = user_input.get_user_menu_choice(menu_options)
    if user_choice is None:
        return actions.restart_menu(context)
    return user_choice(context)
