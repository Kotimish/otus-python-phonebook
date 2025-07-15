import os


def clear_terminal():
    """Очистка терминала"""
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    else:
        print('Ошибка при очистке экрана, неопределенный тип операционной системы')

def render_interface(label: str = 'Меню', extra_info: str=None):
    """Отрисовка интерфейса меню"""
    clear_terminal()
    print(f'=== {label} ===')
    # Отрисовка блока интерфейса под дополнительную информацию
    if extra_info:
        print('=' * (8 + len(label)))
        print(extra_info)
    print('=' * (8 + len(label)))

def render_choice_interface(menu_options: dict):
    """Отрисовка меню с выбором"""
    for key, option in menu_options.items():
        print(f"{key}. {option['label']}")
