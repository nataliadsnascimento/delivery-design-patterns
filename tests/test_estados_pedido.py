import pytest
from states.estados_pedido import (
    ESTADOS,
    ACaminho,
    Cancelado,
    Entregue,
    EstadoPedido,
    Preparando,
    Recebido,
    TransicaoInvalidaError,
)


def test_fluxo_completo_entrega():
    estado: EstadoPedido = Recebido()
    assert estado.nome == "recebido"

    estado = estado.avancar()
    assert isinstance(estado, Preparando)
    assert estado.nome == "preparando"

    estado = estado.avancar()
    assert isinstance(estado, ACaminho)
    assert estado.nome == "a_caminho"

    estado = estado.avancar()
    assert isinstance(estado, Entregue)
    assert estado.nome == "entregue"


@pytest.mark.parametrize("estado_inicial", [Recebido(), Preparando()])
def test_cancelamento_valido(estado_inicial):
    novo_estado = estado_inicial.cancelar()
    assert isinstance(novo_estado, Cancelado)
    assert novo_estado.nome == "cancelado"


@pytest.mark.parametrize("estado_bloqueado", [ACaminho(), Entregue(), Cancelado()])
def test_cancelamento_invalido_lanca_excecao(estado_bloqueado):
    with pytest.raises((TransicaoInvalidaError, ValueError)):
        estado_bloqueado.cancelar()


@pytest.mark.parametrize("estado_final", [Entregue(), Cancelado()])
def test_avancar_estado_final_lanca_excecao(estado_final):
    with pytest.raises((TransicaoInvalidaError, ValueError)):
        estado_final.avancar()


def test_dicionario_estados():
    assert set(ESTADOS.keys()) == {"recebido", "preparando", "a_caminho", "entregue", "cancelado"}
    for chave, classe in ESTADOS.items():
        instancia = classe()
        assert isinstance(instancia, EstadoPedido)
        assert instancia.nome == chave