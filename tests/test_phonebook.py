from pathlib import Path

import pytest

import src.exceptions.phonebook as exceptions
from src import settings
from src.models.contact import Contact
from src.models.phonebook import PhoneBook
from src.repositories.json_repository import JsonRepository


@pytest.fixture()
def phonebook():
    file_path = Path(__file__).parent / 'data' / 'test_phonebook_data.json'
    repository = JsonRepository(str(file_path))
    pb = PhoneBook(repository)
    pb.load_contacts()
    return pb


@pytest.mark.parametrize(
    'name, phone, comment',
    [
        ('Алексеев Алексей Алексеевич', '8(888)888-88-88', ''),
        ('Иванов Иван Иванович', '+7(777)7777777', ''),
        ('Андреев Андрей Андреевич', '12345678900', ''),
        ('Николаев Николай Николаевич', 12345678900, ''),
    ]
)
def test_create_valid_contact(name: str, phone: str | int, comment: str):
    """Тест создания контактов из телефонного справочника"""
    repository = JsonRepository(settings.DEFAULT_CONTACTS_FILE_PATH)
    phonebook = PhoneBook(repository)
    idx = phonebook.create_contact(name, phone, comment)
    contact = phonebook.get_contact(idx)

    assert contact.name == name
    assert contact.phone == str(phone)
    assert contact.comment == comment


@pytest.mark.parametrize(
    'name, phone, comment',
    [
        ('Тестов Тест Тестович', '+9(999)999-99-99', ''),
        ('Jones Smith', '+1-212-456-7890', ''),
        ('Zhang Wei', '+8615555151447', ''),
    ]
)
def test_find_valid_contact_by_phone(phonebook: PhoneBook, name: str, phone: str | int, comment: str):
    """Тест поиска контактов в телефонном справочнике по номеру"""
    test_contact = Contact(name, phone, comment)
    phonebook.create_contact(name, phone, comment)
    found_contacts = phonebook.find_contact(phone)
    assert len(found_contacts) == 1
    for found_contact in found_contacts.values():
        assert found_contact == test_contact


@pytest.mark.parametrize(
    'name, phone, comment',
    [
        ('Тестов Тест Тестович', '+9(999)999-99-99', ''),
        ('Jones Smith', '+1-212-456-7890', ''),
        ('Zhang Wei', '+8615555151447', ''),
    ]
)
def test_find_valid_contact_by_name(phonebook: PhoneBook, name: str, phone: str | int, comment: str):
    """Тест поиска контактов в телефонном справочнике по имени"""
    test_contact = Contact(name, phone, comment)
    phonebook.create_contact(name, phone, comment)
    found_contacts = phonebook.find_contact(name)
    assert len(found_contacts) == 1
    for found_contact in found_contacts.values():
        assert found_contact == test_contact


@pytest.mark.parametrize(
    'name',
    [
        'Тестов Тест Тестович',
        'Jones Smith',
        'Zhang Wei',
    ]
)
def test_find_missing_contact(phonebook: PhoneBook, name: str):
    """Тест некорректного поиска отсутствующего контактов в телефонном справочнике"""
    found_contacts = phonebook.find_contact(name)
    assert len(found_contacts) == 0


@pytest.mark.parametrize(
    'name, phone, comment',
    [
        ('Тестов Тест Тестович', '+9(999)999-99-99', ''),
        ('Jones Smith', '+1-212-456-7890', ''),
        ('Zhang Wei', '+8615555151447', ''),
    ]
)
def test_delete_valid_contact(phonebook: PhoneBook, name: str, phone: str | int, comment: str):
    """Тест удаления контактов из телефонного справочника"""
    # Изначальное число контактов
    origin_count_contacts = len(phonebook.contacts)
    test_contact = Contact(name, phone, comment)
    # Новый контакт для удаления
    idx = phonebook.create_contact(name, phone, comment)
    deleted_contact = phonebook.delete_contact(idx)
    assert deleted_contact == test_contact
    assert origin_count_contacts == len(phonebook.contacts)


def test_get_not_founded_contact(phonebook: PhoneBook):
    """Тест некорректного удаления несуществующего контактов из телефонного справочника"""
    false_idx = len(phonebook.contacts) + 1
    with pytest.raises(exceptions.ContactNotFoundError) as e:
        phonebook.get_contact(false_idx)


@pytest.mark.parametrize(
    'idx',
    [
        0,
        '0',
        None,
    ]
)
def test_get_contact_by_invalid_id(phonebook: PhoneBook, idx: int):
    """Тест некорректного удаления контакта по некорректному ID"""
    with pytest.raises(exceptions.InvalidContactIDError) as e:
        phonebook.get_contact(idx)


@pytest.mark.parametrize(
    'name, phone, new_name',
    [
        ('Иванов Иван Иванович', '8(888)888-88-88', 'Алексеев Алексей Алексеевич'),
        ('Иванов Иван Иванович', '8(888)888-88-88' , 'Jones Smith'),
        ('Иванов Иван Иванович', '8(888)888-88-88', '123456'),
    ]
)
def test_edit_contact_by_name(phonebook: PhoneBook, name: str, phone: str | int, new_name: str):
    """Тестирование изменения имени у контакта из телефонной книги"""
    test_contact = Contact(new_name, phone)
    idx = phonebook.create_contact(name, phone)
    contact = phonebook.get_contact(idx)
    contact.name = new_name
    assert test_contact == contact


@pytest.mark.parametrize(
    'name, phone, new_phone',
    [
        ('Алексеев Алексей Алексеевич', '8(888)888-88-88', '7(777)7777777'),
        ('Николаев Николай Николаевич', 12345678900, 98765432100),
    ]
)
def test_edit_contact_by_phone(phonebook: PhoneBook, name: str, phone: str | int, new_phone: str | int):
    """Тестирование изменения телефона контакта из телефонной книги"""
    test_contact = Contact(name, new_phone)
    idx = phonebook.create_contact(name, phone)
    contact = phonebook.get_contact(idx)
    contact.phone = new_phone
    assert test_contact == contact
