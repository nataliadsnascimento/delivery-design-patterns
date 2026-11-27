from typing import List, Optional, Union

from models.cliente import Cliente
from models.item import Item
from observers.observador import Observador   #16
from states.estados_pedido import ESTADOS, EstadoPedido, Recebido

TIPOS_VALIDOS = ("local", "retirada", "entrega")


class Pedido:

    def __init__(
        self,
        cliente: Cliente,
        tipo: str = "local",
        frete=None,
        desconto=None,
        estado: Optional[EstadoPedido] = None,
    ):
        if tipo not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo de pedido inválido: {tipo}")
        self.id: Optional[int] = None
        self.cliente = cliente
        self.tipo = tipo
        self.itens: List[Item] = []
        self.frete = frete
        self.desconto = desconto
        self.estado: EstadoPedido = estado if estado is not None else Recebido()
        self._observadores = []

    @property
    def status(self) -> str:
        return self.estado.nome

    @status.setter
    def status(self, valor: Union[str, EstadoPedido]) -> None:
        if isinstance(valor, EstadoPedido):
            self.estado = valor
        elif isinstance(valor, str) and valor in ESTADOS:
            self.estado = ESTADOS[valor]()
        else:
            raise ValueError(f"Status inválido: {valor}")

    def avancar(self) -> None:
        self.estado = self.estado.avancar()
        self.notificar() #16

    def cancelar(self) -> None:
        self.estado = self.estado.cancelar()
        self.notificar() #16

    def adicionar_item(self, item: Item) -> None:
        if not isinstance(item, Item):
            raise TypeError("Só é possível adicionar objetos do tipo Item")
        self.itens.append(item)

    def subtotal(self) -> float:
        return round(sum(item.preco() for item in self.itens), 2)

    def valor_frete(self) -> float:
        return round(self.frete.calcular(self), 2) if self.frete else 0.0

    def valor_desconto(self) -> float:
        return round(self.desconto.calcular(self), 2) if self.desconto else 0.0

    def total(self) -> float:
        base = max(self.subtotal() - self.valor_desconto(), 0.0)
        return round(base + self.valor_frete(), 2)
        

    # --- Observer (#16): o Pedido é o Subject ---
    def adicionar_observador(self, observador: Observador) -> None:
        if not isinstance(observador, Observador):
            raise TypeError("Só é possível registrar objetos do tipo Observador")
        if observador not in self._observadores:
            self._observadores.append(observador)

    def remover_observador(self, observador: Observador) -> None:
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar(self) -> None:
        # Itera sobre uma cópia: um observador pode se remover durante o aviso.
        for observador in list(self._observadores):
            observador.atualizar(self, self.status)
    