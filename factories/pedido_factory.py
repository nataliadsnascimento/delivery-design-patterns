from abc import ABC, abstractmethod

from models.cliente import Cliente
from models.pedido import Pedido


class PedidoFactory(ABC):

    @abstractmethod
    def criar(self, cliente: Cliente) -> Pedido:
        """Cria um pedido."""
        pass


class PedidoEntregaFactory(PedidoFactory):

    def criar(self, cliente: Cliente) -> Pedido:

        if not cliente.endereco or not cliente.endereco.strip():
            raise ValueError(
                "O endereço é obrigatório para pedidos de entrega."
            )

        return Pedido(cliente=cliente, tipo="entrega")


class PedidoRetiradaFactory(PedidoFactory):

    def criar(self, cliente: Cliente) -> Pedido:

        return Pedido(cliente=cliente, tipo="retirada")


class PedidoLocalFactory(PedidoFactory):

    def criar(self, cliente: Cliente) -> Pedido:

        return Pedido(cliente=cliente, tipo="local")