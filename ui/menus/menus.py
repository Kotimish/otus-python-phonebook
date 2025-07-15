from core import actions
from ui import render, user_input


def welcome_menu(context: dict) -> str:
    """
    Меню входа в приложение
    """
    menu_name = 'Добро пожаловать'
    menu_options = {
        '1': {'label': 'Открыть телефонный справочник', 'action': actions.open_phonebook},
        '2': {'label': 'Выбрать другой телефонный справочник', 'action': actions.change_phonebook},
        '0': {'label': 'Выход', 'action': actions.close_app},
    }
    if (
        'file' in context and
        context['file']
    ):
        text = (
            f'Выбран телефонный справочник из файла: {context["file"]}'
        )
    else:
        text = ''
    render.render_interface(menu_name, extra_info=text)
    render.render_choice_interface(menu_options)
    user_choice = user_input.get_user_menu_choice(menu_options)
    if user_choice is None:
        return actions.restart_menu(context)
    return user_choice(context)

def main_menu(context: dict) -> str:
    """Основное меню"""

    menu_name = 'Телефонный справочник'
    menu_options = {
        '1': {'label': 'Показать все контакты', 'action': actions.show_all_contacts},
        '2': {'label': 'Поиск контакта', 'action': lambda _: 'contact_search_menu'},
        '3': {'label': 'Создание контакта', 'action': actions.create_contact},
        '4': {'label': 'Сохранить', 'action': actions.save_phonebook},
        '5': {'label': 'Сохранить как...', 'action': actions.save_phonebook_in_another_file},
        '0': {'label': 'Выход', 'action': actions.close_phonebook},
    }
    text = (
        f'Загружен телефонный справочник из файла: {context["file"]}.'
        # f'\nНайдено контактов: {len(context["phonebook"])}.'
    )
    if context['is_modified']:
        text += (
            '\nБыли внесены изменения в телефонный справочник.'
            '\nРекомендуется сохранить.'
        )
    render.render_interface(menu_name, extra_info=text)
    render.render_choice_interface(menu_options)
    user_choice = user_input.get_user_menu_choice(menu_options)
    if user_choice is None:
        return actions.go_back_menu(context)
    return user_choice(context)
