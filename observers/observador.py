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
     
#17
def _status_legivel(status: str) -> str:               
    return status.replace("_", " ").capitalize()       


def _numero(pedido: "Pedido") -> str:                  
    return f"#{pedido.id}" if pedido.id is not None else "(novo)"
   


class NotificadorCliente(Observador):                  
    def atualizar(self, pedido: "Pedido", status: str) -> None:
        print(
            f"[Cliente] {pedido.cliente.nome}, "
            f"seu pedido {_numero(pedido)} agora está: {_status_legivel(status)}"
        )


class PainelCozinha(Observador):                       
    def atualizar(self, pedido: "Pedido", status: str) -> None:
        itens = ", ".join(item.descricao() for item in pedido.itens) or "sem itens"
        print(
            f"[Cozinha] Pedido {_numero(pedido)} ({pedido.tipo}) -> "
            f"{_status_legivel(status)} | Itens: {itens}"
        )
        def _status_legivel(status: str) -> str:
    """Transforma 'a_caminho' em 'A caminho' para mostrar na tela."""
    return status.replace("_", " ").capitalize()


def _numero(pedido: "Pedido") -> str:
    """Pedido ainda não salvo no banco não tem id."""
    return f"#{pedido.id}" if pedido.id is not None else "(novo)"


class NotificadorCliente(Observador):
    def atualizar(self, pedido: "Pedido", status: str) -> None:
        print(
            f"[Cliente] {pedido.cliente.nome}, "
            f"seu pedido {_numero(pedido)} agora está: {_status_legivel(status)}"
        )


class PainelCozinha(Observador):
    def atualizar(self, pedido: "Pedido", status: str) -> None:
        itens = ", ".join(item.descricao() for item in pedido.itens) or "sem itens"
        print(
            f"[Cozinha] Pedido {_numero(pedido)} ({pedido.tipo}) -> "
            f"{_status_legivel(status)} | Itens: {itens}"
        )
