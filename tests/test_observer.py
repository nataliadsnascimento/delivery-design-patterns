from unittest.mock import Mock

import pytest

from models.cliente import Cliente
from models.pedido import Pedido
from observers.observador import Observador
from states.estados_pedido import TransicaoInvalidaError


class ObservadorFalso(Observador):
    def __init__(self):
        self.avisos = []

    def atualizar(self, pedido, status):
        self.avisos.append((pedido, status))


@pytest.fixture
def pedido():
    cliente = Cliente(nome="Ana", telefone="81 99999-0000", endereco="Rua A, 1")
    return Pedido(cliente, tipo="entrega")


def test_observador_e_abstrato():
    with pytest.raises(TypeError):
        Observador()


def test_observador_registrado_e_avisado_ao_avancar(pedido):
    obs = ObservadorFalso()
    pedido.adicionar_observador(obs)

    pedido.avancar()

    assert obs.avisos == [(pedido, "preparando")]


def test_todos_os_observadores_recebem_o_aviso(pedido):
    a, b = ObservadorFalso(), ObservadorFalso()
    pedido.adicionar_observador(a)
    pedido.adicionar_observador(b)

    pedido.avancar()

    assert len(a.avisos) == 1
    assert len(b.avisos) == 1


def test_avisa_a_cada_mudanca_de_estado(pedido):
    obs = ObservadorFalso()
    pedido.adicionar_observador(obs)

    pedido.avancar()
    pedido.avancar()
    pedido.avancar()

    assert [status for _, status in obs.avisos] == ["preparando", "a_caminho", "entregue"]


def test_cancelar_tambem_notifica(pedido):
    obs = ObservadorFalso()
    pedido.adicionar_observador(obs)

    pedido.cancelar()

    assert obs.avisos == [(pedido, "cancelado")]


def test_observador_removido_nao_recebe_mais(pedido):
    obs = ObservadorFalso()
    pedido.adicionar_observador(obs)
    pedido.remover_observador(obs)

    pedido.avancar()

    assert obs.avisos == []


def test_remover_quem_nao_esta_registrado_nao_da_erro(pedido):
    pedido.remover_observador(ObservadorFalso())


def test_mesmo_observador_nao_e_registrado_duas_vezes(pedido):
    obs = ObservadorFalso()
    pedido.adicionar_observador(obs)
    pedido.adicionar_observador(obs)

    pedido.avancar()

    assert len(obs.avisos) == 1


def test_so_aceita_observador(pedido):
    with pytest.raises(TypeError):
        pedido.adicionar_observador("cozinha")


def test_transicao_invalida_nao_notifica(pedido):
    obs = ObservadorFalso()
    pedido.cancelar()
    pedido.adicionar_observador(obs)

    with pytest.raises(TransicaoInvalidaError):
        pedido.avancar()

    assert obs.avisos == []


def test_atualizar_recebe_pedido_e_status_usando_mock(pedido):
    obs = Mock(spec=Observador)
    pedido.adicionar_observador(obs)

    pedido.avancar()

    obs.atualizar.assert_called_once_with(pedido, "preparando")


def test_mudar_status_pelo_setter_nao_notifica(pedido):
    obs = ObservadorFalso()
    pedido.adicionar_observador(obs)

    pedido.status = "a_caminho"

    assert obs.avisos == []