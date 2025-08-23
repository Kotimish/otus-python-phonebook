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
    with pytest.raises(exceptions.LoadingRepositoryDataError) as e:
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


def test_save_phonebook_with_missing_file(tmp_path):
    """Тест некорректного сохранения справочника"""
    file_path = tmp_path / 'test_phonebook_data.json'
    repository = JsonRepository(str(file_path))
    phonebook = PhoneBook(repository)
    phonebook.repository.file_path = tmp_path / 'missing_dir' / 'test_phonebook_data.json'
    with pytest.raises(exceptions.RepositoryPathError) as e:
        phonebook.save_contacts()


def test_save_phonebook_with_invalid_data(tmp_path):
    """Тест сохранения справочника с некорректными данными"""
    data = {1, 2, 3}
    file_path = tmp_path / 'test_phonebook_data.json'
    repository = JsonRepository(str(file_path))
    with pytest.raises(exceptions.SavingRepositoryDataError) as e:
        repository.save(data)