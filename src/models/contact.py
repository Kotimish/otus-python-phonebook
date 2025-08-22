import re

from src.exceptions.contact import InvalidPhoneNumberError, InvalidContactNameError


class Contact:
    """Класс для работы с контактами"""
    def __init__(self, name: str, phone: str, comment: str=''):
        self.name = name
        self._phone = ''
        self.phone = phone
        self.comment = comment
        # Только после всех присваиваний
        self.fields = [
            self.name,
            self.phone,
            self.comment
        ]

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise InvalidContactNameError(value)
        self._name = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        if not self._is_phone_number(value):
            raise InvalidPhoneNumberError(value)
        self._phone = value

    def __str__(self):
        text = (
            f'Имя: {self.name}, '
            f'Телефон: {self.phone}'
        )
        if self.comment:
            text += f', Коммент: {self.comment};'
        return text

    def contains(self, word: str) -> bool:
        """
        Проверка на вхождение строки в атрибуты контакта
        :param word: Искомое слово
        :return: True, если нашлось вхождение, иначе False
        """
        for field in self.fields:
            if word.lower() in field.lower():
                return True
        return False

    def serialize(self):
        """
        Преобразует контакт в словарь
        :return:
        """
        return {
            'name': self.name,
            'phone': self.phone,
            'comment': self.comment
        }

    @classmethod
    def deserialize(cls, data: dict):
        """
        Создает экземпляр класса Contact на основе данных словаря
        :param data: Словарь с данными
        :return: экземпляр класса Contact
        """
        return cls(
            data.get('name'),
            data.get('phone'),
            data.get('comment'),
        )

    @staticmethod
    def _is_phone_number(number: str) -> bool:
        """
        Проверка строки на принадлежность к телефонному номеру.
        Телефонный номер должен иметь спец символ + в начале,
        должен быть длинной от 7 до 15 символов, включая код страны
        и может иметь спец символы (Скобки, пробельные символы, дефисы и тире)
        :param number: Проверяемая строка с телефонным номером
        :return: True, если строка является телефонным номером, иначе False
        """
        # Список разрешенных спец-символов в телефонном номере
        # Скобки, пробельные символы, дефисы и тире
        pattern = r'[\(\)\s\u002D\u2010\u2011\u2012\u2013\u2014\u2212]+'
        # Отсутствует номер
        if not number:
            return False
        # Пропущен указатель на международный код страны
        if len(number) > 0 and number[0] != '+':
            return False
        number = number[1:]
        number = re.sub(pattern, '', number)
        # В номере присутствуют недопустимые символы
        if not number.isdigit():
            return False
        # Некорректная длина телефонного номера
        if not (7 <= len(number) <= 15):
            return False
        return True