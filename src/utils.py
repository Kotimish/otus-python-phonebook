import os


def clear_terminal(self):
    """Очистка терминала"""
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    else:
        self.show_message('Ошибка при очистке экрана, неопределенный тип операционной системы')
