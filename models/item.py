from abc import ABC, abstractmethod


class Item(ABC):

    @abstractmethod
    def descricao(self) -> str:
        """Texto exibido para o cliente."""

    @abstractmethod
    def preco(self) -> float:
        """Preço do item em reais."""