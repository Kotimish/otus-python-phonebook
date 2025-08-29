from abc import ABC, abstractmethod
from src.models.contact import Contact


class AbstractView(ABC):
    """Интерфейс для представления"""
    @abstractmethod
    def show_message(self, message: str) -> None:
        """Отображение сообщения."""
        raise NotImplementedError

    @abstractmethod
    def show_menu(self, title: str, options: list) -> None:
        """Отображение меню."""
        raise NotImplementedError

    @abstractmethod
    def show_contacts(self, phonebook: list[tuple[int, str]], error_message: str) -> None:
        """Отображение списка контактов."""
        raise NotImplementedError

    @abstractmethod
    def get_user_menu_choice(self, max_choice: int) -> int:
        """Выбор пункта меню пользователем."""
        raise NotImplementedError

    @abstractmethod
    def get_user_input(self, message: str | list[str]) -> str | list[str]:
        """Запрос данных от пользователя."""
        raise NotImplementedError

    @abstractmethod
    def confirm_action(self, question: str, default: str = "yes") -> bool:
        """Получение подтверждения пользователя на закрытый вопрос"""
        raise NotImplementedError

