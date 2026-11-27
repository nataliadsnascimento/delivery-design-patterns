"""Interface do padrão Observer (#16)."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.pedido import Pedido


class Observador(ABC):
    @abstractmethod
    def atualizar(self, pedido: "Pedido", status: str) -> None:
