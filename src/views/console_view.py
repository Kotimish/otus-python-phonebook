from src import text, settings
from src.interfaces.view import AbstractView


class ConsoleView(AbstractView):
    CONFIRM_MAP = {
        "yes": True, "y": True, "no": False, "n": False,
        "да": True, "д": True, "нет": False, "н": False,
    }

    def show_message(self, message: str):
        """
        Отображает переданное сообщение пользователю
        :param message: Текст сообщения
        """
        print(message)

    def show_menu(self, title: str, options: list[str]):
        """
        Отрисовывает меню
        :param title: Название меню
        :param options: Доступные опции
        """
        print(title)
        for number, item in enumerate(options, start=1):
            self.show_message(f'\t{number}. {item}')

    def show_contacts(self, phonebook: list[tuple[int, str]], error_message: str):
        """
        Отображает переданные контакты
        :param phonebook: Список контактов в формате (id, краткая информация о контакте)
        :param error_message: Сообщение об ошибки в случае пустого словаря
        """
        if not phonebook:
            self.show_message(error_message)
            return
        for idx, contact in phonebook:
            self.show_message(text.show_contact.format(idx=idx, contact=contact))

    def get_user_menu_choice(self, max_choice: int) -> int:
        """
        Получение и обработка выбора пункта меню от пользователя
        :param max_choice: число пунктов для выбора пользователем
        :return: возвращает соответствующее действие для выбранного пункта меню
        """
        while True:
            user_choice = self.get_user_input(text.user_menu_choice).strip()
            if (
                    user_choice.isdigit() and
                    0 < int(user_choice) <= max_choice
            ):
                return int(user_choice)
            print(text.user_menu_choice_error.format(menu_options=max_choice))

    def get_user_input(self, message: str | list[str]) -> str | list[str]:
        """
        Получает от пользователя ввод данных
        :param message: Сообщение для пользователя с запросом данных
        :return: строку или список из строк с ответом пользователя
        """
        if isinstance(message, str):
            message = [message]
        result = []
        for msg in message:
            sub_result = ''
            while not sub_result:
                try:
                    sub_result = input(msg)
                except UnicodeDecodeError:
                    self.show_message(text.decode_error)
                    continue
                else:
                    break
            result.append(sub_result)

        return result if len(result) > 1 else result[0]

    def confirm_action(self, question: str, default: str = "yes") -> bool:
        """
        Создание и получения ответа пользователя на закрытый вопрос
        :param question: текст закрытого вопроса
        :param default: ответ по умолчанию
        :return: возвращает True для положительного ответа и False для отрицательного
        """
        error_message = ''
        attempt_count = 0
        while attempt_count < settings.MAX_USER_INPUT_ATTEMPTS:
            if error_message:
                print(error_message)
            user_input = input(f"{question} (y/n): ").strip().lower()
            if not user_input:
                user_input = default
            if user_input in self.CONFIRM_MAP:
                return self.CONFIRM_MAP[user_input]
            error_message = text.incorrect_input_close_answer_error
            attempt_count += 1
        self.show_message(text.maximum_number_attempts_error.format(default=default))
        self.get_user_input(text.press_any_key)
        return self.CONFIRM_MAP[default]
