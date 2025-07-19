import json
from model.contact import Contact
from model.file_handler import FileHandler


class PhoneBook:
    """Класс для работы с телефонным справочником"""
    def __init__(self, path):
        self.path = path
        self.contacts = {}

    def create_contact(self, contact: list) -> int:
        """
        Создает контакт на основе введенных данных
        :param contact: Данные нового контакта
        :return: ID нового контакта
        """
        next_id = self._next_id()
        self.contacts[next_id] = Contact(
            contact[0],
            contact[1],
            contact[2]
        )
        return next_id

    def get_contact(self, contact_id: int) -> dict:
        """
        Получение контакта из Телефонного справочника
        :param contact_id: ID искомого контакта
        :return: Контакт
        """
        return self.contacts.get(contact_id)

    def _next_id(self) -> int:
        """
        Отдают следующий свободный id
        :return: Доступный ID
        """
        return max(self.contacts, default=0) + 1

    def find_contact(self, word: str) -> dict[int, Contact]:
        """
        Поиск контакт(а/ов) по ключевому слову
        :param word: искомое слово
        :return: Словарь из всех найденных контактов
        """
        result_pb = {}
        for idx, contact in self.contacts.items():
            if contact.contains(word):
                result_pb[idx] = contact
        return result_pb

    def edit_contact(self, contact_id: int, edited_contact: dict[str, str]) -> dict:
        """
        Изменить контакт
        :param contact_id: ID изменяемого контакта
        :param edited_contact: Данные для изменения
        :return: Словарь с данными об измененном контакте
        """
        origin_contact = self.get_contact(contact_id)
        if 'name' in edited_contact and edited_contact['name']:
            origin_contact.name = edited_contact['name']
        if 'phone' in edited_contact and edited_contact['phone']:
            origin_contact.phone = edited_contact['phone']
        if 'comment' in edited_contact and edited_contact['comment']:
            origin_contact.comment = edited_contact['comment']
        return origin_contact

    def delete_contact(self, contact_id: int) -> Contact:
        """
        Удалить контакт
        :param contact_id: ID удаляемого контакта
        :return: Словарь с данными об удаленном контакте
        """
        contact = self.contacts.pop(contact_id)
        return contact

    def load_json(self):
        """
        Загрузка json-файла
        """
        data = FileHandler.load_json(self.path)
        self.contacts = {
            idx: Contact.deserialize(contact)
            for idx, contact in enumerate(data.get('phonebook', []), 1)
        }

    def save_json(self):
        """
        Сохранение json-файла
        """
        data = {'phonebook': []}
        for contact in self.contacts.values():
            data['phonebook'].append(contact.serialize())
        FileHandler.save_json(self.path, data)
