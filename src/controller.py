import src.exceptions.contact
import src.exceptions.phonebook
from src import text
from src import utils
from src.model.phonebook import PhoneBook
from src.view.console_view import ConsoleView


class MainController:
    """Основной обработчик"""
    def __init__(self, phonebook: PhoneBook, view: ConsoleView):
        self.phonebook = phonebook
        self.view = view
        self.is_running = True

    def open_phonebook(self):
        if (
                len(self.phonebook.contacts) > 0 and
                not utils.ask_yes_no(text.exist_phonebook_error, default='no')
        ):
            return
        try:
            self.phonebook.load_json()
        # todo переделать в кастомную ошибку
        except FileNotFoundError as e:
            self.view.show_message(text.error.format(error=e))
        except src.exceptions.phonebook.InvalidJSONError as e:
            self.view.show_message(text.error.format(error=e))
        else:
            self.view.show_message(text.phonebook_load_successful)

    def save_phonebook(self):
        self.phonebook.save_json()
        self.view.show_message(text.phonebook_save_successful)

    def show_contacts(self):
        self.view.show_contacts(self.phonebook.contacts, text.empty_phonebook_error)


    def find_contact(self):
        find_word = self.view.input_date(text.input_find_word)
        found_contacts = self.phonebook.find_contact(find_word)
        self.view.show_contacts(found_contacts, text.no_found_contact.format(word=find_word))

    def create_contact(self):
        data = self.view.input_date([
            text.input_contact_name,
            text.input_contact_phone,
            text.input_contact_comment,
        ])
        try:
            self.phonebook.create_contact(data)
        except src.exceptions.contact.InvalidPhoneNumberError as e:
            self.view.show_message(text.error.format(error=e))
        else:
            self.view.show_message(text.contact_created_successful.format(name=data[0]))

    def edit_contact(self):
        contact_id = self.view.input_date(text.input_id_contact)
        if not contact_id.isdigit():
            self.view.show_message(text.input_id_contact_error)
            return
        contact_id = int(contact_id)
        new_data = self.view.input_date(text.input_contact_data_to_edit)
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
            self.view.show_message(text.contact_edited_successful.format(name=edited_contact['name']))

    def delete_contact(self):
        contact_id = self.view.input_date(text.input_id_contact)
        if not contact_id.isdigit():
            self.view.show_message(text.input_id_contact_error)
            return
        contact_id = int(contact_id)

        user_confirm = utils.ask_yes_no(text.confirm_delete_contact, default='no')
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
            user_choice = self.view.get_user_menu_choice(options)
            menu_actions[user_choice - 1]()
        else:
            self.view.show_message(text.end_of_program)
            self.view.input_date(text.press_any_key)
            exit()
