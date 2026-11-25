import pytest

from models.cliente import Cliente
from models.item import Item
from models.pedido import Pedido


class ItemFalso(Item):
    def __init__(self, preco):
        self._preco = preco

    def descricao(self):
        return "item"

    def preco(self):
        return self._preco


class ValorFixo:

    def __init__(self, valor):
        self.valor = valor

    def calcular(self, pedido):
        return self.valor


class Metade:

    def calcular(self, pedido):
        return pedido.subtotal() * 0.5


@pytest.fixture
def cliente():
    return Cliente(nome="Ana", telefone="81 99999-0000")


def test_pedido_novo_comeca_vazio(cliente):
    p = Pedido(cliente)
    assert p.subtotal() == 0
    assert p.total() == 0
    assert p.status == "recebido"


def test_tipo_invalido(cliente):
    with pytest.raises(ValueError):
        Pedido(cliente, tipo="viagem")


def test_adicionar_so_aceita_item(cliente):
    p = Pedido(cliente)
    with pytest.raises(TypeError):
        p.adicionar_item("pizza")


def test_subtotal_soma_os_itens(cliente):
    p = Pedido(cliente)
    p.adicionar_item(ItemFalso(30.0))
    p.adicionar_item(ItemFalso(12.5))
    assert p.subtotal() == 42.5


def test_total_com_frete(cliente):
    p = Pedido(cliente, tipo="entrega", frete=ValorFixo(5.0))
    p.adicionar_item(ItemFalso(40.0))
    assert p.total() == 45.0


def test_total_com_desconto_e_frete(cliente):
    p = Pedido(cliente, tipo="entrega", frete=ValorFixo(5.0), desconto=ValorFixo(10.0))
    p.adicionar_item(ItemFalso(40.0))
    assert p.total() == 35.0


def test_desconto_maior_que_subtotal_nao_fica_negativo(cliente):
    p = Pedido(cliente, tipo="entrega", frete=ValorFixo(5.0), desconto=ValorFixo(50.0))
    p.adicionar_item(ItemFalso(10.0))
    assert p.total() == 5.0


def test_estrategia_que_usa_subtotal_nao_causa_recursao(cliente):
    p = Pedido(cliente, desconto=Metade())
    p.adicionar_item(ItemFalso(20.0))
    assert p.total() == 10.0


def test_trocar_estrategia_em_tempo_de_execucao(cliente):
    p = Pedido(cliente, tipo="entrega", frete=ValorFixo(5.0))
    p.adicionar_item(ItemFalso(40.0))
    assert p.total() == 45.0
    p.frete = ValorFixo(0.0)
    assert p.total() == 40.0