import settings
import states


def create_context():
    """Создание дефолтного передаваемого контекста"""
    return {
        # Путь к файлу
        'file': settings.DEFAULT_CONTACTS_FILE_PATH,
        # Список всех контакты
        'phonebook': [],
        # История состояний
        'history': [],
        # Текущий контакт(ы)
        'current_contact': {},
        'current_contacts': [],
        # Указание на изменение справочника
        'is_modified': False,
        # Счетчик id для корректного создания новых записей
        'max_id': -1,
    }


def init_menu():
    """Центральная функция инициации вспомогательных элементов"""
    states.init()


def state_handler(default_menu: str):
    """
    Обработчик состояний в виде конечного автомата
    """
    context = create_context()
    # Начальный статус
    current_state = default_menu

    while current_state != 'exit':
        next_state = states.get_state(current_state)(context)
        # Перезапуск текущего меню
        if next_state == 'current_menu':
            continue
        # Возврат в предыдущее меню
        if next_state == 'back_menu':
            if len(context['history']) > 0:
                current_state = context['history'].pop()
            else:
                current_state = default_menu
        else:
            if next_state != current_state:
                context['history'].append(current_state)
            current_state = next_state

    input('Нажмите Enter для завершения работы...')


if __name__=='__main__':
    init_menu()
    state_handler('welcome_menu')
