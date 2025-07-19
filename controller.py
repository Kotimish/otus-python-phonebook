import settings
import text
import view
from model import phonebook


def run():
    """
    Центральный обработчик логики приложения
    """
    is_running = True
    while is_running:
        menu = text.main_menu_items.get('title', '')
        options = text.main_menu_items.get('items', [])
        view.show_menu(menu, options)
        user_choice = view.get_user_menu_choice(options)

        if user_choice == 1:
            phonebook.load_json(settings.DEFAULT_CONTACTS_FILE_PATH)
            view.show_message(text.phonebook_load_successful)
        elif user_choice == 2:
            phonebook.save_json(settings.DEFAULT_CONTACTS_FILE_PATH)
            view.show_message(text.phonebook_save_successful)
        elif user_choice == 3:
            view.show_contacts(phonebook.phonebook, text.empty_phonebook_error)
        elif user_choice == 4:
            data = view.input_date([
                text.input_contact_name,
                text.input_contact_phone,
                text.input_contact_comment,
            ])
            phonebook.create_contact({
                'name': data[0],
                'phone': data[1],
                'comment': data[2],
            })
            view.show_message(text.contact_created_successful.format(name=data[0]))
        elif user_choice == 5:
            find_word = view.input_date(text.input_find_word)
            found_contacts = phonebook.find_contact(find_word)
            view.show_contacts(found_contacts, text.no_found_contact.format(word=find_word))
        elif user_choice == 6:
            contact_id = view.input_date(text.input_id_contact)
            if not contact_id.isdigit():
                view.show_message(text.input_id_contact_error)
                continue
            contact_id = int(contact_id)
            new_data = view.input_date(text.input_contact_data_to_edit)
            new_data = {
                'name': new_data[0],
                'phone': new_data[1],
                'comment': new_data[2],
            }
            edited_contact = phonebook.edit_contact(contact_id, new_data)
            view.show_message(text.contact_edited_successful.format(name=edited_contact['name']))
        elif user_choice == 7:
            contact_id = view.input_date(text.input_id_contact)
            if not contact_id.isdigit():
                view.show_message(text.input_id_contact_error)
                continue
            contact_id = int(contact_id)
            contact = phonebook.delete_contact(contact_id)
            view.show_message(text.contact_deleted_successful.format(name=contact['name']))
        elif user_choice == 8:
            is_running = False
        else:
            is_running = False

    view.show_message(text.end_of_program)
    view.input_date(text.press_any_key)
    exit()
