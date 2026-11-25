import pytest
from models.item import Item
from models.itens import Bebida, Hamburguer, Pizza, Sobremesa


@pytest.mark.parametrize(
    "classe, nome_esperado, preco_esperado",
    [
        (Hamburguer, "Hambúrguer Artesanal", 28.0),
        (Pizza, "Pizza Mussarela", 45.0),
        (Bebida, "Refrigerante Lata", 7.0),
        (Sobremesa, "Pudim", 12.0),
    ],
)
def test_item_concreto_valores_padrao(classe, nome_esperado, preco_esperado):
    item = classe()
    assert isinstance(item, Item)
    assert item.descricao() == nome_esperado
    assert item.preco() == preco_esperado


def test_item_concreto_customizado():
    pizza = Pizza(nome="Pizza Calabresa", preco_base=52.5)
    assert pizza.descricao() == "Pizza Calabresa"
    assert pizza.preco() == 52.5