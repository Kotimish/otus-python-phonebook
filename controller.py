import view
import text
from model.phonebook import PhoneBook


class MainController:
    def __init__(self, file_path):
        self.phonebook = PhoneBook(file_path)

    def open_phonebook(self):
        self.phonebook.load_json()
        view.show_message(text.phonebook_load_successful)


    def save_phonebook(self):
        self.phonebook.save_json()
        view.show_message(text.phonebook_save_successful)


    def show_contacts(self):
        view.show_contacts(self.phonebook.contacts, text.empty_phonebook_error)


    def find_contact(self):
        find_word = view.input_date(text.input_find_word)
        found_contacts = self.phonebook.find_contact(find_word)
        view.show_contacts(found_contacts, text.no_found_contact.format(word=find_word))


    def create_contact(self):
        data = view.input_date([
            text.input_contact_name,
            text.input_contact_phone,
            text.input_contact_comment,
        ])
        self.phonebook.create_contact(data)
        view.show_message(text.contact_created_successful.format(name=data[0]))


    def edit_contact(self):
        contact_id = view.input_date(text.input_id_contact)
        if not contact_id.isdigit():
            view.show_message(text.input_id_contact_error)
            return
        contact_id = int(contact_id)
        new_data = view.input_date(text.input_contact_data_to_edit)
        new_data = {
            'name': new_data[0],
            'phone': new_data[1],
            'comment': new_data[2],
        }
        edited_contact = self.phonebook.edit_contact(contact_id, new_data)
        view.show_message(text.contact_edited_successful.format(name=edited_contact['name']))


    def delete_contact(self):
        contact_id = view.input_date(text.input_id_contact)
        if not contact_id.isdigit():
            view.show_message(text.input_id_contact_error)
            return
        contact_id = int(contact_id)
        contact = self.phonebook.delete_contact(contact_id)
        view.show_message(text.contact_deleted_successful.format(name=contact.name))


    def exit_app(self):
        view.show_message(text.end_of_program)
        view.input_date(text.press_any_key)
        exit()

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

        is_running = True
        while is_running:
            # Отрисовка меню
            menu = text.main_menu_items.get('title', '')
            options = text.main_menu_items.get('items', [])
            view.show_menu(menu, options)
            # Опции меню
            user_choice = view.get_user_menu_choice(options)
            menu_actions[user_choice - 1]()
