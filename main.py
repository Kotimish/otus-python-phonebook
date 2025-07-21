import settings
from controller import MainController


if __name__=='__main__':
    controller = MainController(settings.DEFAULT_CONTACTS_FILE_PATH)
    controller.run()
