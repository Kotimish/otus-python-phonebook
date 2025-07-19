import settings
import text
import view


def ask_yes_no(question: str, default: str = "yes"):
    """
    Создание и получения ответа пользователя на закрытый вопрос
    :param question: текст закрытого вопроса
    :param default: ответ по умолчанию
    :return: возвращает True для положительного ответа и False для отрицательного
    """
    valid_input = {
        "yes": True, "y": True, "no": False, "n": False,
        "да": True, "д": True, "нет": False, "н": False,
    }
    error_message = ''
    attempt_count = 0
    while attempt_count < settings.MAX_USER_INPUT_ATTEMPTS:
        if error_message:
            print(error_message)
        user_input = input(f"{question} (y/n): ").strip().lower()
        if not user_input:
            user_input = default
        if user_input in valid_input:
            return valid_input[user_input]
        error_message = text.incorrect_input_close_answer_error
        attempt_count += 1
    view.show_message(text.maximum_number_attempts_error.format(default=default))
    view.input_date(text.press_any_key)
    return valid_input[default]
