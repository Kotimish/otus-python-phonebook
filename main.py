import locale
import sys

import settings
from controller import MainController


if __name__=='__main__':
    print("Кодировка stdin:", sys.stdin.encoding)
    print("Кодировка stdout:", sys.stdout.encoding)
    print("Кодировка stderr:", sys.stderr.encoding)

    print("Локаль системы:", locale.getpreferredencoding())

    controller = MainController(settings.DEFAULT_CONTACTS_FILE_PATH)
    controller.run()
