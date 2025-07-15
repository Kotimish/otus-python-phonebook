

def get_max_id(contacts):
    """
    Получение максимального id среди контактов для добавления новых уникальных id
    :param contacts: Список контактов
    :return: Максимальный id
    """
    max_id = -1
    if not contacts or not isinstance(contacts, list):
        print('Ошибка. Получен некорректный список контактов')
        return max_id

    for contact in contacts:
        if (
            'id' not in contact
        ):
            continue
        contact_id = contact['id']
        if (
            contact_id and
            contact_id.isdigit() and
            int(contact_id) > max_id
        ):
            max_id = int(contact_id)
    return max_id
