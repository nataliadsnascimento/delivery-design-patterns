import pytest

from adicionais.decoradores import (
    ADICIONAIS,
    AdicionalDecorator,
    Bacon,
    BordaRecheada,
    EmbalagemPresente,
    QueijoExtra,
)
from models.cliente import Cliente
from models.item import Item
from models.itens import Hamburguer, Pizza
from models.pedido import Pedido


def test_adicional_abstrato_nao_pode_ser_instanciado():
    with pytest.raises(TypeError):
        AdicionalDecorator(Pizza())

def test_adicional_exige_um_item():
    with pytest.raises(TypeError):
        Bacon("não é um item")

def test_decorador_e_um_item():
    assert isinstance(Bacon(Pizza()), Item)

def test_um_adicional():
    item = BordaRecheada(Pizza())

    assert item.descricao() == "Pizza Mussarela + Borda Recheada"
    assert item.preco() == 53.00

def test_combinacao_de_adicionais():
    item = Bacon(QueijoExtra(Hamburguer()))

    assert item.descricao() == "Hambúrguer Artesanal + Queijo Extra + Bacon"
    assert item.preco() == 39.0


def test_adicionais_nao_alteram_o_item_original():
    pizza = Pizza()
    BordaRecheada(pizza)

    assert pizza.descricao() == "Pizza Mussarela"
    assert pizza.preco() == 45.0


def test_mesmo_adicional_duas_vezes():
    item = QueijoExtra(QueijoExtra(Pizza()))

    assert item.descricao() == "Pizza Mussarela + Queijo Extra + Queijo Extra"
    assert item.preco() == 55.0


def test_ordem_muda_a_descricao_mas_nao_o_preco():
    a = Bacon(BordaRecheada(Pizza()))
    b = BordaRecheada(Bacon(Pizza()))

    assert a.descricao() == "Pizza Mussarela + Borda Recheada + Bacon"
    assert b.descricao() == "Pizza Mussarela + Bacon + Borda Recheada"
    assert a.preco() == b.preco() == 59.0


def test_embalagem_presente():
    item = EmbalagemPresente(Pizza())

    assert item.descricao() == "Pizza Mussarela + Embalagem Presente"
    assert item.preco() == 48.0


def test_item_acessivel_pela_cadeia():
    pizza = Pizza()
    item = Bacon(BordaRecheada(pizza))

    assert item.item.item is pizza


def test_dicionario_adicionais():
    assert set(ADICIONAIS) == {
        "borda_recheada", "queijo_extra", "bacon", "embalagem_presente",
    }
    assert ADICIONAIS["bacon"] is Bacon


def test_adicional_escolhido_pelo_dicionario():
    item = ADICIONAIS["queijo_extra"](Pizza())

    assert item.preco() == 50.0


def test_item_decorado_entra_no_pedido():
    pedido = Pedido(
        cliente=Cliente(nome="Maria", telefone="87900000001"),
        tipo="local",
    )
    pedido.adicionar_item(Bacon(Hamburguer()))
    pedido.adicionar_item(Pizza())

    assert pedido.subtotal() == 79.0