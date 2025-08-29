import pytest

import src.exceptions.contact as exceptions
from src.models.contact import Contact


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
    """Тест на создание контакта с корректными данными"""
    contact = Contact(name, phone, comment)
    assert contact.name == name
    assert contact.phone == str(phone)
    assert contact.comment == comment


@pytest.mark.parametrize(
    'name, phone, comment',
    [
        ('Иванов Иван Иванович', '', ''),
        ('Иванов Иван Иванович', '123456789101112131415', ''),
        ('Иванов Иван Иванович', {}, ''),
        ('Иванов Иван Иванович', None, ''),
    ]
)
def test_create_contact_with_invalid_phone(name: str, phone: str | int, comment: str):
    """Тест на создание контакта с некорректным номером телефона"""
    with pytest.raises(exceptions.InvalidPhoneNumberError) as e:
        Contact(name, phone, comment)


@pytest.mark.parametrize(
    'name, phone, comment',
    [
        ('', '', ''),
        ('', '8(888)888-88-88', ''),
        (None, '8(888)888-88-88', ''),
    ]
)
def test_create_contact_with_invalid_name(name: str, phone: str | int, comment: str):
    """Тест на создание контакта с некорректным именем"""
    with pytest.raises(exceptions.InvalidContactNameError) as e:
        Contact(name, phone, comment)


@pytest.mark.parametrize(
    'name, phone, comment, new_phone',
    [
        ('Алексеев Алексей Алексеевич', '8(888)888-88-88', '', '7(777)7777777'),
        ('Николаев Николай Николаевич', 12345678900, '', 98765432100),
    ]
)
def test_edit_valid_contact_phone(name: str, phone: str | int, comment: str, new_phone: str):
    """Тест на изменение номера контакта"""
    contact = Contact(name, phone, comment)
    contact.phone = new_phone
    assert contact.phone == str(new_phone)


@pytest.mark.parametrize(
    'name, phone, comment, new_phone',
    [
        ('Иванов Иван Иванович', '8(888)888-88-88', '', ''),
        ('Иванов Иван Иванович', '8(888)888-88-88', '', '123456789101112131415'),
        ('Иванов Иван Иванович', '8(888)888-88-88', '', {}),
        ('Иванов Иван Иванович', '8(888)888-88-88', '', None),
    ]
)
def test_edit_invalid_contact_phone(name: str, phone: str | int, comment: str, new_phone: str):
    """Тест на некорректное изменение номера контакта"""
    contact = Contact(name, phone, comment)
    with pytest.raises(exceptions.InvalidPhoneNumberError) as e:
        contact.phone = new_phone


@pytest.mark.parametrize(
    'name, phone, new_name',
    [
        ('Иванов Иван Иванович', '8(888)888-88-88', 'Алексеев Алексей Алексеевич'),
        ('Иванов Иван Иванович', '8(888)888-88-88', 'Jones Smith'),
        ('Иванов Иван Иванович', '8(888)888-88-88',  '123456'),
    ]
)
def test_edit_valid_contact_name(name: str, phone: str | int, new_name: str):
    """Тест на изменение названия контакта"""
    contact = Contact(name, phone)
    contact.name = new_name
    assert contact.name == new_name


@pytest.mark.parametrize(
    'name, phone, comment, new_name',
    [
        ('Иванов Иван Иванович', '8(888)888-88-88', '', ''),
        ('Иванов Иван Иванович', '8(888)888-88-88', '', 123456),
        ('Иванов Иван Иванович', '8(888)888-88-88', '', {}),
        ('Иванов Иван Иванович', '8(888)888-88-88', '', None),
    ]
)
def test_edit_invalid_contact_name(name: str, phone: str | int, comment: str, new_name: str):
    """Тест на некорректное изменение названия контакта"""
    contact = Contact(name, phone, comment)
    with pytest.raises(exceptions.InvalidContactNameError) as e:
        contact.name = new_name