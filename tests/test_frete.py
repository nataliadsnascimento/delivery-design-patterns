import pytest

from models.cliente import Cliente
from models.itens import Bebida, Pizza
from models.pedido import Pedido
from strategies.frete import (
    FRETES,
    EstrategiaFrete,
    FreteFixo,
    FreteGratis,
    FretePorDistancia,
)


@pytest.fixture
def pedido():
    p = Pedido(
        cliente=Cliente(nome="Maria", telefone="87900000001", endereco="Rua A, 100"),
        tipo="entrega",
    )
    p.adicionar_item(Pizza())
    p.adicionar_item(Bebida())
    return p


def test_estrategia_abstrata_nao_pode_ser_instanciada():

    with pytest.raises(TypeError):
        EstrategiaFrete()


def test_frete_fixo(pedido):

    assert FreteFixo(8.0).calcular(pedido) == 8.0


def test_frete_por_distancia(pedido):

    estrategia = FretePorDistancia(5, taxa_base=3.0, valor_por_km=2.0)

    assert estrategia.calcular(pedido) == 13.0


def test_frete_por_distancia_negativa():

    with pytest.raises(ValueError):
        FretePorDistancia(-1)


def test_frete_gratis_acima_do_limite(pedido):

    assert FreteGratis(frete_gratis_acima=50.0).calcular(pedido) == 0.0


def test_frete_gratis_abaixo_do_limite_cobra_frete_base(pedido):

    estrategia = FreteGratis(frete_gratis_acima=100.0, frete_base=FreteFixo(8.0))

    assert estrategia.calcular(pedido) == 8.0


def test_dicionario_fretes():

    assert set(FRETES) == {"fixo", "distancia", "gratis"}
    assert FRETES["fixo"] is FreteFixo
    assert all(classe.nome == nome for nome, classe in FRETES.items())


def test_pedido_sem_frete(pedido):

    assert pedido.total() == pedido.subtotal()


def test_troca_de_estrategia_em_tempo_de_execucao(pedido):

    pedido.frete = FreteFixo(8.0)
    assert pedido.total() == 60.0

    pedido.frete = FreteGratis(frete_gratis_acima=50.0)
    assert pedido.total() == 52.0

    pedido.frete = FretePorDistancia(5, taxa_base=3.0, valor_por_km=2.0)
    assert pedido.total() == 65.0