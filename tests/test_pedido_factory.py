import pytest

from models.cliente import Cliente
from models.pedido import Pedido

from factories.pedido_factory import (
    PedidoFactory,
    PedidoEntregaFactory,
    PedidoRetiradaFactory,
    PedidoLocalFactory,
)


def test_factory_abstrata():
    with pytest.raises(TypeError):
        PedidoFactory()


def test_pedido_entrega():
    cliente = Cliente(
        nome="Maria",
        telefone="87900000001",
        endereco="Rua A, 100"
    )

    factory = PedidoEntregaFactory()
    pedido = factory.criar(cliente)

    assert isinstance(pedido, Pedido)
    assert pedido.tipo == "entrega"
    assert pedido.cliente is cliente


def test_pedido_entrega_sem_endereco():
    cliente = Cliente(
        nome="Maria",
        telefone="87900000001"
    )

    factory = PedidoEntregaFactory()

    with pytest.raises(ValueError):
        factory.criar(cliente)


def test_pedido_entrega_endereco_vazio():
    cliente = Cliente(
        nome="Maria",
        telefone="87900000001",
        endereco="   "
    )

    factory = PedidoEntregaFactory()

    with pytest.raises(ValueError):
        factory.criar(cliente)


def test_pedido_retirada():
    cliente = Cliente(
        nome="João",
        telefone="87900000002"
    )

    factory = PedidoRetiradaFactory()
    pedido = factory.criar(cliente)

    assert isinstance(pedido, Pedido)
    assert pedido.tipo == "retirada"
    assert pedido.cliente is cliente


def test_pedido_local():
    cliente = Cliente(
        nome="Ana",
        telefone="87900000003"
    )

    factory = PedidoLocalFactory()
    pedido = factory.criar(cliente)

    assert isinstance(pedido, Pedido)
    assert pedido.tipo == "local"
    assert pedido.cliente is cliente