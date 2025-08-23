from src.exceptions.phonebook import InvalidContactIDError, ContactNotFoundError
from src.interfaces.repository import AbstractRepository
from src.models.contact import Contact


class PhoneBook:
    """Класс для работы с телефонным справочником"""
    def __init__(self, repository: AbstractRepository):
        self.repository = repository
        self.contacts: dict[int, Contact] = {}

    def create_contact(self, name: str, phone: str, comment: str = '') -> int:
        """
        Создает контакт на основе введенных данных
        :param name: Название контакта
        :param phone: Номер телефона
        :param comment: Комментарий (опционально)
        :return: ID нового контакта
        """
        next_id = self._next_id()
        self.contacts[next_id] = Contact(name, phone, comment)
        return next_id

    def get_contact(self, contact_id: int) -> Contact:
        """
        Получение контакта из Телефонного справочника
        :param contact_id: ID искомого контакта
        :return: Контакт
        """
        self._check_contact_id(contact_id)
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

    def edit_contact(self, contact_id: int, edited_contact: dict[str, str]) -> Contact:
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
        self._check_contact_id(contact_id)
        contact = self.contacts.pop(contact_id)
        return contact

    def _check_contact_id(self, contact_id: int):
        """Проверка корректности id контакта"""
        if not isinstance(contact_id, int) or contact_id <= 0:
            raise InvalidContactIDError(contact_id)
        if contact_id not in self.contacts:
            raise ContactNotFoundError(contact_id)

    def load_contacts(self):
        """
        Загрузка json-файла
        """
        data = self.repository.load()
        self.contacts = {
            idx: Contact.deserialize(contact)
            for idx, contact in enumerate(data.get('phonebook', []), 1)
        }

    def save_contacts(self):
        """
        Сохранение json-файла
        """
        data = {'phonebook': []}
        for contact in self.contacts.values():
            data['phonebook'].append(contact.serialize())
        self.repository.save(data)
