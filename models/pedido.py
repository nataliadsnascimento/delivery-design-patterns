from typing import List, Optional

from models.cliente import Cliente
from models.item import Item

TIPOS_VALIDOS = ("local", "retirada", "entrega")


class Pedido:

    def __init__(self, cliente: Cliente, tipo: str = "local", frete=None, desconto=None):
        if tipo not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo de pedido inválido: {tipo}")
        self.id: Optional[int] = None 
        self.cliente = cliente
        self.tipo = tipo
        self.itens: List[Item] = []
        self.frete = frete
        self.desconto = desconto
        self.status = "recebido"  
        self._observadores = []  

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