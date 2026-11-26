import pytest

from models.cliente import Cliente
from models.item import Item


def test_cliente_valores_padrao():
    c = Cliente(nome="Ana", telefone="81 99999-0000")
    assert c.endereco is None
    assert c.primeira_compra is True
    assert c.id is None


def test_item_nao_pode_ser_instanciado():
    with pytest.raises(TypeError):
        Item()


def test_item_concreto_funciona():
    class ItemFalso(Item):
        def descricao(self):
            return "teste"

        def preco(self):
            return 10.0

    assert ItemFalso().preco() == 10.0