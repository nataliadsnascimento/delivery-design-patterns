import pytest

from models.cliente import Cliente
from models.itens import Pizza, Bebida
from models.pedido import Pedido
from observers.observador import NotificadorCliente, PainelCozinha


@pytest.fixture
def pedido():
    cliente = Cliente(nome="Maria Silva", telefone="81 99999-0000", endereco="Rua A, 1")
    p = Pedido(cliente, tipo="entrega")
    p.id = 12
    p.adicionar_item(Pizza())
    p.adicionar_item(Bebida())
    return p


def test_cliente_recebe_mensagem_clara(pedido, capsys):
    pedido.adicionar_observador(NotificadorCliente())

    pedido.avancar()

    saida = capsys.readouterr().out
    assert "[Cliente]" in saida
    assert "Maria Silva" in saida
    assert "#12" in saida
    assert "Preparando" in saida


def test_cozinha_mostra_pedido_tipo_status_e_itens(pedido, capsys):
    pedido.adicionar_observador(PainelCozinha())

    pedido.avancar()

    saida = capsys.readouterr().out
    assert "[Cozinha]" in saida
    assert "#12" in saida
    assert "entrega" in saida
    assert "Preparando" in saida
    assert "Pizza Mussarela" in saida


def test_status_com_underline_vira_texto_legivel(pedido, capsys):
    pedido.adicionar_observador(NotificadorCliente())

    pedido.avancar()
    pedido.avancar()

    assert "A caminho" in capsys.readouterr().out


def test_os_dois_sao_avisados_na_mesma_mudanca(pedido, capsys):
    pedido.adicionar_observador(NotificadorCliente())
    pedido.adicionar_observador(PainelCozinha())

    pedido.avancar()

    saida = capsys.readouterr().out
    assert "[Cliente]" in saida
    assert "[Cozinha]" in saida


def test_cancelamento_tambem_aparece(pedido, capsys):
    pedido.adicionar_observador(NotificadorCliente())

    pedido.cancelar()

    assert "Cancelado" in capsys.readouterr().out


def test_pedido_sem_id_mostra_novo(capsys):
    cliente = Cliente(nome="Ana", telefone="1")
    p = Pedido(cliente)
    p.adicionar_observador(NotificadorCliente())

    p.avancar()

    assert "(novo)" in capsys.readouterr().out


def test_pedido_sem_itens_na_cozinha(capsys):
    cliente = Cliente(nome="Ana", telefone="1")
    p = Pedido(cliente)
    p.adicionar_observador(PainelCozinha())

    p.avancar()

    assert "sem itens" in capsys.readouterr().out