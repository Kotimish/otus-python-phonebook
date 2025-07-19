# Телефонный справочник
## Инструкция 
### Клонировать репозиторий
1. По HTTP
    ```bash
    git clone https://github.com/Kotimish/otus-python-phonebook.git
    ```
2. Или по SSH
    ```bash
    git clone github.com:Kotimish/otus-python-phonebook.git
    ```
3. Перейти в созданную папку проекта
    ```bash
    cd otus-python-phonebook
    ```
### Виртуальное окружение
```bash
python3 -m venv .venv
source .venv/bin/activate
```
PS: Убедитесь, что ваша версия Python не ниже 3.6
При необходимости указывайте явно версию Python при создании окружения
К примеру (для Python3.11)
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```
В дальнейшем при работе в виртуальном окружении будет использоваться по умолчанию указанная ранее версия
### Установка пакетов
```bash
pip3 install -r requirements.txt
```

### Запуск
```bash
    python main.py
```
