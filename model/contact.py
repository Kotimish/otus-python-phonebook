from model import validation


class Contact:
    """Класс для работы с контактами"""
    def __init__(self, name, phone, comment=''):
        self.name = name
        self._phone = ''
        self.phone = phone
        self.comment = comment
        self.fields = [
            self.name,
            self.phone,
            self.comment
        ]

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        if not validation.is_phone_number(value):
            return
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
        return Contact(
            data.get('name'),
            data.get('phone'),
            data.get('comment'),
        )