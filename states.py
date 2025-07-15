from ui.menus.base_menu import missing_menu


def create_router():
    """
    Функция работы с состояниями посредством замыкания
    """

    # Состояния и ссылки на используемые интерфейсы
    states = {
        'missing_menu': missing_menu
    }


    def register_state(function, state_name: str):
        """
        Ручная регистрация состояний в обработчике
        :param function: Регистрируемая функция отрисовки меню
        :param state_name: Регистрируемый статус для обработчика
        """
        if state_name in states:
            print(f'Ошибка: статус {state_name} уже зарегистрирован')
        else:
            states[state_name] = function
            print(f'Статус {state_name} успешно зарегистрирован')


    def get_state(state_name: str):
        """Получение ссылки на зарегистрированную функцию через состояние"""
        return states.get(state_name, missing_menu)

    return register_state, get_state


def init():
    """Явная регистрация интерфейсов меню"""
    # Регистрация основных меню
    from ui.menus.menus import main_menu, welcome_menu
    from ui.menus.contact import contact_menu, contacts_menu
    from ui.menus.contact import change_contact_menu
    from ui.menus.search_menus import contact_search_menu

    register_state(welcome_menu, 'welcome_menu')
    register_state(main_menu, 'main_menu')
    register_state(contact_menu, 'contact_menu')
    register_state(contacts_menu, 'contacts_menu')
    register_state(change_contact_menu, 'change_contact_menu')
    register_state(contact_search_menu, 'contact_search_menu')

register_state, get_state = create_router()
