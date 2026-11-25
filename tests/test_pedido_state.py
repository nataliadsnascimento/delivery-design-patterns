import pytest

from models.cliente import Cliente
from models.pedido import Pedido
from states.estados_pedido import (
    ACaminho,
    Cancelado,
    Entregue,
    Preparando,
    Recebido,
    TransicaoInvalidaError,
)


@pytest.fixture
def pedido():
    cliente = Cliente(nome="João", telefone="11999999999", endereco="Rua A, 123")
    return Pedido(cliente=cliente, tipo="entrega")


def test_pedido_inicia_no_estado_recebido(pedido):
    assert isinstance(pedido.estado, Recebido)
    assert pedido.status == "recebido"


def test_pedido_avanca_ate_entregue(pedido):
    pedido.avancar()
    assert isinstance(pedido.estado, Preparando)
    assert pedido.status == "preparando"

    pedido.avancar()
    assert isinstance(pedido.estado, ACaminho)
    assert pedido.status == "a_caminho"

    pedido.avancar()
    assert isinstance(pedido.estado, Entregue)
    assert pedido.status == "entregue"


def test_pedido_pode_ser_cancelado_enquanto_recebido_ou_preparando(pedido):
    pedido.cancelar()
    assert isinstance(pedido.estado, Cancelado)
    assert pedido.status == "cancelado"

    cliente2 = Cliente(nome="Maria", telefone="11888888888", endereco="Rua B, 456")
    pedido2 = Pedido(cliente=cliente2, tipo="retirada")
    pedido2.avancar()  # preparando
    pedido2.cancelar()
    assert isinstance(pedido2.estado, Cancelado)
    assert pedido2.status == "cancelado"


def test_pedido_nao_cancela_a_caminho_ou_entregue(pedido):
    pedido.avancar()  # preparando
    pedido.avancar()  # a_caminho

    with pytest.raises((TransicaoInvalidaError, ValueError)):
        pedido.cancelar()
    assert pedido.status == "a_caminho"

    pedido.avancar()  # entregue
    with pytest.raises((TransicaoInvalidaError, ValueError)):
        pedido.cancelar()
    assert pedido.status == "entregue"


def test_pedido_finalizado_ou_cancelado_nao_avanca(pedido):
    pedido.cancelar()
    with pytest.raises((TransicaoInvalidaError, ValueError)):
        pedido.avancar()


def test_setter_status_reconstroi_estado(pedido):
    pedido.status = "a_caminho"
    assert isinstance(pedido.estado, ACaminho)
    assert pedido.status == "a_caminho"

    with pytest.raises(ValueError):
        pedido.status = "inexistente"