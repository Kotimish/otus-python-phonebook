from pathlib import Path


# Дефолтные настройки
BASE_DIR = Path(__file__).parent

FILE_DIR = "data"

DEFAULT_CONTACTS_FILE_PATH = BASE_DIR / FILE_DIR / "contacts.json"

MAX_USER_INPUT_ATTEMPTS = 3

MAX_SHOW_CONTACTS = 10
