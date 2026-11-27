"""Observer: notificadores e log (#16, #17, #18)"""

#--#   python -m unittest discover -s tests -p "test_*.py" -v

#16
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.pedido import Pedido


class Observador(ABC):
    @abstractmethod
    def atualizar(self, pedido: "Pedido", status: str) -> None:
     """Chamado pelo pedido a cada mudança de estado."""
     

