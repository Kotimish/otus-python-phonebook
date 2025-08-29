from src import settings
from src.controllers.main_controller import MainController
from src.repositories.json_repository import JsonRepository
from src.models.phonebook import PhoneBook
from src.views.console_view import ConsoleView

if __name__=='__main__':
    repository = JsonRepository(settings.DEFAULT_CONTACTS_FILE_PATH)
    phonebook = PhoneBook(repository)
    view = ConsoleView()

    controller = MainController(phonebook, view)
    controller.run()
