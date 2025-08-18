from src import settings
from src.controller import MainController
from src.model.phonebook import PhoneBook
from src.view.console_view import ConsoleView

if __name__=='__main__':
    phonebook = PhoneBook(settings.DEFAULT_CONTACTS_FILE_PATH)
    view = ConsoleView()

    controller = MainController(phonebook, view)
    controller.run()
