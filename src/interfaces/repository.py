from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def load(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: dict):
        raise NotImplementedError
