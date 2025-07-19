import states
import controller
from handler import state_handler

def init_menu():
    """Центральная функция инициации вспомогательных элементов"""
    states.init()


if __name__=='__main__':
    # deprecated logic
    # init_menu()
    # state_handler('welcome_menu')
    controller.run()
