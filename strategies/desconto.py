from abc import ABC, abstractmethod

from models.pedido import Pedido


class EstrategiaDesconto(ABC):
    """Contrato: calcular(pedido) devolve o valor a abater (positivo).

    Use pedido.subtotal(), nunca pedido.total() (recursão infinita).
    """

    nome: str = ""

    @abstractmethod
    def calcular(self, pedido: Pedido) -> float:
        """Devolve o valor do desconto em reais."""


class SemDesconto(EstrategiaDesconto):
    nome = "sem_desconto"

    def calcular(self, pedido: Pedido) -> float:
        return 0.0


class CupomPercentual(EstrategiaDesconto):
    nome = "cupom"

    def __init__(self, percentual: float) -> None:
        if not 0 <= percentual <= 100:
            raise ValueError("O percentual deve estar entre 0 e 100.")
        self._percentual = percentual

    def calcular(self, pedido: Pedido) -> float:
        return pedido.subtotal() * self._percentual / 100


class PrimeiraCompra(EstrategiaDesconto):
    nome = "primeira_compra"

    def __init__(self, percentual: float = 10.0) -> None:
        if not 0 <= percentual <= 100:
            raise ValueError("O percentual deve estar entre 0 e 100.")
        self._percentual = percentual

    def calcular(self, pedido: Pedido) -> float:
        if not pedido.cliente.primeira_compra:
            return 0.0
        return pedido.subtotal() * self._percentual / 100


DESCONTOS = {
    SemDesconto.nome: SemDesconto,
    CupomPercentual.nome: CupomPercentual,
    PrimeiraCompra.nome: PrimeiraCompra,
}