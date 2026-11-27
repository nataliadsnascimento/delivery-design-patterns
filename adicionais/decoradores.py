from abc import abstractmethod

from models.item import Item


class AdicionalDecorator(Item):
    """Embrulha um Item e acrescenta um adicional ao texto e ao preço."""

    def __init__(self, item: Item) -> None:
        if not isinstance(item, Item):
            raise TypeError("O adicional só pode decorar objetos do tipo Item")
        self._item = item

    @property
    @abstractmethod
    def nome(self) -> str:
        """Nome do adicional, exibido na descrição."""

    @property
    @abstractmethod
    def preco_adicional(self) -> float:
        """Valor acrescentado ao preço do item."""

    @property
    def item(self) -> Item:
        """Item embrulhado por este adicional."""
        return self._item

    def descricao(self) -> str:
        return f"{self._item.descricao()} + {self.nome}"

    def preco(self) -> float:
        return self._item.preco() + self.preco_adicional


class BordaRecheada(AdicionalDecorator):
    nome = "Borda Recheada"
    preco_adicional = 8.0


class QueijoExtra(AdicionalDecorator):
    nome = "Queijo Extra"
    preco_adicional = 5.0


class Bacon(AdicionalDecorator):
    nome = "Bacon"
    preco_adicional = 6.0


class EmbalagemPresente(AdicionalDecorator):
    nome = "Embalagem Presente"
    preco_adicional = 3.0

ADICIONAIS = {
    "borda_recheada": BordaRecheada,
    "queijo_extra": QueijoExtra,
    "bacon": Bacon,
    "embalagem_presente": EmbalagemPresente,
}