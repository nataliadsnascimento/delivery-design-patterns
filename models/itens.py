"""Itens concretos do cardápio."""

from models.item import Item


class Hamburguer(Item):
    def __init__(self, nome: str = "Hambúrguer Artesanal", preco_base: float = 28.0) -> None:
        self._nome = nome
        self._preco_base = preco_base

    def descricao(self) -> str:
        return self._nome

    def preco(self) -> float:
        return self._preco_base


class Pizza(Item):
    def __init__(self, nome: str = "Pizza Mussarela", preco_base: float = 45.0) -> None:
        self._nome = nome
        self._preco_base = preco_base

    def descricao(self) -> str:
        return self._nome

    def preco(self) -> float:
        return self._preco_base


class Bebida(Item):
    def __init__(self, nome: str = "Refrigerante Lata", preco_base: float = 7.0) -> None:
        self._nome = nome
        self._preco_base = preco_base

    def descricao(self) -> str:
        return self._nome

    def preco(self) -> float:
        return self._preco_base


class Sobremesa(Item):
    def __init__(self, nome: str = "Pudim", preco_base: float = 12.0) -> None:
        self._nome = nome
        self._preco_base = preco_base

    def descricao(self) -> str:
        return self._nome

    def preco(self) -> float:
        return self._preco_base