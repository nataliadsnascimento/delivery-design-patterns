from abc import ABC, abstractmethod

from models.pedido import Pedido


class EstrategiaFrete(ABC):
    """Contrato: calcular(pedido) devolve o valor do frete.

    Use pedido.subtotal(), nunca pedido.total() (recursão infinita).
    """

    nome: str = ""

    @abstractmethod
    def calcular(self, pedido: Pedido) -> float:
        """Devolve o valor do frete em reais."""


class FreteFixo(EstrategiaFrete):
    nome = "fixo"

    def __init__(self, valor: float = 8.0) -> None:  # AJUSTAR: valor padrão
        self._valor = valor

    def calcular(self, pedido: Pedido) -> float:
        return self._valor


class FretePorDistancia(EstrategiaFrete):
    nome = "distancia"

    def __init__(
        self,
        distancia_km: float,
        taxa_base: float = 3.0,
        valor_por_km: float = 2.0,
    ) -> None:
        if distancia_km < 0:
            raise ValueError("A distância não pode ser negativa.")
        self._distancia_km = distancia_km
        self._taxa_base = taxa_base
        self._valor_por_km = valor_por_km

    def calcular(self, pedido: Pedido) -> float:
        return self._taxa_base + self._distancia_km * self._valor_por_km


class FreteGratis(EstrategiaFrete):
    nome = "gratis"

    def __init__(
        self,
        frete_gratis_acima: float,
        frete_base: EstrategiaFrete = None,
    ) -> None:
        self._limite = frete_gratis_acima
        self._frete_base = frete_base if frete_base is not None else FreteFixo()

    def calcular(self, pedido: Pedido) -> float:
        if pedido.subtotal() >= self._limite:
            return 0.0
        return self._frete_base.calcular(pedido)

FRETES = {
    FreteFixo.nome: FreteFixo,
    FretePorDistancia.nome: FretePorDistancia,
    FreteGratis.nome: FreteGratis,
}