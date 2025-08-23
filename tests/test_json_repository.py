import json
from pathlib import Path

import pytest

from src.models.contact import Contact
from src.models.phonebook import PhoneBook
import src.exceptions.repository as exceptions
from src.repositories.json_repository import JsonRepository


def test_load_phonebook():
    """Тест загрузки справочника"""
    file_path = Path(__file__).parent / 'data' / 'test_phonebook_data.json'
    repository = JsonRepository(str(file_path))
    phonebook = PhoneBook(repository)
    phonebook.load_contacts()
    assert len(phonebook.contacts) > 0


def test_load_phonebook_with_missing_file():
    """Тест некорректной загрузки справочника по некорректному пути"""
    file_path = Path(__file__).parent / 'data' / 'missing_test_phonebook_data.json'
    repository = JsonRepository(str(file_path))
    phonebook = PhoneBook(repository)
    with pytest.raises(exceptions.RepositoryPathError) as e:
        phonebook.load_contacts()


def test_load_phonebook_with_invalid_file_type():
    """Тест некорректной загрузки справочника с некорректным форматов данных"""
    file_path = Path(__file__).parent / 'data' / 'test_phonebook_data.csv'
    repository = JsonRepository(str(file_path))
    phonebook = PhoneBook(repository)
    with pytest.raises(exceptions.IncorrectRepositoryDataError) as e:
        phonebook.load_contacts()


def test_save_valid_phonebook(tmp_path):
    """Тест сохранения справочника"""
    # Подготовка тестовых данных
    name = 'Тестов Тест Тестович'
    phone = '+9(999)999-99-99'
    comment = 'Тестовый комментарий'
    test_contact = Contact(name, phone, comment)

    file_path = tmp_path / 'test_phonebook_data.json'
    repository = JsonRepository(str(file_path))
    phonebook = PhoneBook(repository)
    # Заполнение
    phonebook.create_contact(name, phone, comment)
    phonebook.save_contacts()
    # Проверка
    assert file_path.exists()
    # Заново загружаем
    phonebook.load_contacts()
    assert len(phonebook.contacts) == 1
    for idx, contact in phonebook.contacts.items():
        assert test_contact == contact