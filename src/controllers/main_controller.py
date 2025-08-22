import src.exceptions.contact
import src.exceptions.phonebook
from src import text
from src.interfaces.view import AbstractView
from src.models.contact import Contact
from src.models.phonebook import PhoneBook


class MainController:
    """Основной обработчик"""
    def __init__(self, phonebook: PhoneBook, view: AbstractView):
        self.phonebook = phonebook
        self.view = view
        self.is_running = True

    def open_phonebook(self):
        if (
                len(self.phonebook.contacts) > 0 and
                not self.view.confirm_action(text.exist_phonebook_error, default='no')
        ):
            return
        try:
            self.phonebook.load_contacts()
        except FileNotFoundError as e:
            self.view.show_message(text.error.format(error=e))
        except src.exceptions.phonebook.InvalidJSONError as e:
            self.view.show_message(text.error.format(error=e))
        else:
            self.view.show_message(text.phonebook_load_successful)

    def save_phonebook(self):
        self.phonebook.save_contacts()
        self.view.show_message(text.phonebook_save_successful)

    def show_contacts(self):
        contacts = self._format_contacts()
        self.view.show_contacts(contacts, text.empty_phonebook_error)


    def find_contact(self):
        find_word = self.view.get_user_input(text.input_find_word)
        found_contacts = self.phonebook.find_contact(find_word)
        found_contacts = self._format_contacts(found_contacts)
        self.view.show_contacts(found_contacts, text.no_found_contact.format(word=find_word))

    def create_contact(self):
        name, phone, comment = self.view.get_user_input([
            text.input_contact_name,
            text.input_contact_phone,
            text.input_contact_comment,
        ])
        try:
            self.phonebook.create_contact(name, phone, comment)
        except src.exceptions.contact.InvalidPhoneNumberError as e:
            self.view.show_message(text.error.format(error=e))
        else:
            self.view.show_message(text.contact_created_successful.format(name=name))

    def edit_contact(self):
        contact_id = self._get_valid_contact_id()
        if contact_id is None:
            return

        new_data = self.view.get_user_input(text.input_contact_data_to_edit)
        new_data = {
            'name': new_data[0],
            'phone': new_data[1],
            'comment': new_data[2],
        }
        try:
            edited_contact = self.phonebook.edit_contact(contact_id, new_data)
        except src.exceptions.phonebook.InvalidContactIDError as e:
            self.view.show_message(text.error.format(error=e))
        except src.exceptions.phonebook.ContactNotFoundError as e:
            self.view.show_message(text.error.format(error=e))
        else:
            self.view.show_message(text.contact_edited_successful.format(name=edited_contact.name))

    def delete_contact(self):
        contact_id = self._get_valid_contact_id()
        if contact_id is None:
            return

        user_confirm = self.view.confirm_action(text.confirm_delete_contact, default='no')
        if not user_confirm:
            self.view.show_message(text.cancel_operation)
            return
        try:
            contact = self.phonebook.delete_contact(contact_id)
        except src.exceptions.phonebook.InvalidContactIDError as e:
            self.view.show_message(text.error.format(error=e))
        except src.exceptions.phonebook.ContactNotFoundError as e:
            self.view.show_message(text.error.format(error=e))
        else:
            self.view.show_message(text.contact_deleted_successful.format(name=contact.name))

    def exit_app(self):
        self.is_running = False

    def _get_valid_contact_id(self) -> int | None:
        """Проверка на получение от пользователя корректного ID"""
        user_input = self.view.get_user_input(text.input_id_contact)
        if not user_input.isdigit():
            self.view.show_message(text.input_id_contact_error)
            return None
        return int(user_input)

    def _format_contacts(self, contacts: dict[int, Contact] | None = None) -> list[tuple[int, str]]:
        """Преобразование контактов в корректный для представления вид"""
        if contacts is None:
            contacts = self.phonebook.contacts
        return [
            (idx, str(contact))
            for idx, contact in contacts.items()
        ]

    def run(self):
        """
        Центральный обработчик логики приложения
        """
        menu_actions = [
            self.open_phonebook,
            self.save_phonebook,
            self.show_contacts,
            self.create_contact,
            self.find_contact,
            self.edit_contact,
            self.delete_contact,
            self.exit_app
        ]
        menu = text.main_menu_items.get('title', '')
        options = text.main_menu_items.get('items', [])

        while self.is_running:
            # Отрисовка меню
            self.view.show_menu(menu, options)
            # Опции меню
            user_choice = self.view.get_user_menu_choice(len(options))
            menu_actions[user_choice - 1]()
        else:
            self.view.show_message(text.end_of_program)
            self.view.get_user_input(text.press_any_key)
