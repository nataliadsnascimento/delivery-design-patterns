import pytest

from models.cliente import Cliente
from models.itens import Bebida, Pizza
from models.pedido import Pedido
from strategies.desconto import (
    DESCONTOS,
    CupomPercentual,
    EstrategiaDesconto,
    PrimeiraCompra,
    SemDesconto,
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
        EstrategiaDesconto()


def test_sem_desconto(pedido):
    assert SemDesconto().calcular(pedido) == 0.0


def test_cupom_percentual(pedido):
    assert CupomPercentual(10).calcular(pedido) == pytest.approx(5.2)


def test_cupom_percentual_limites(pedido):
    assert CupomPercentual(0).calcular(pedido) == 0.0
    assert CupomPercentual(100).calcular(pedido) == pytest.approx(52.0)


@pytest.mark.parametrize("percentual", [-1, 101])
def test_cupom_percentual_invalido(percentual):
    with pytest.raises(ValueError):
        CupomPercentual(percentual)


def test_primeira_compra_aplica_desconto(pedido):
    assert pedido.cliente.primeira_compra is True
    assert PrimeiraCompra(10).calcular(pedido) == pytest.approx(5.2)


def test_primeira_compra_cliente_antigo_sem_desconto(pedido):
    pedido.cliente.primeira_compra = False

    assert PrimeiraCompra(10).calcular(pedido) == 0.0


def test_primeira_compra_percentual_invalido():
    with pytest.raises(ValueError):
        PrimeiraCompra(150)


def test_dicionario_descontos():
    assert set(DESCONTOS) == {"sem_desconto", "cupom", "primeira_compra"}
    assert DESCONTOS["cupom"] is CupomPercentual
    assert all(classe.nome == nome for nome, classe in DESCONTOS.items())


def test_pedido_sem_desconto(pedido):
    assert pedido.valor_desconto() == 0.0
    assert pedido.total() == pedido.subtotal()


def test_troca_de_estrategia_tempo_execucao(pedido):
    pedido.desconto = CupomPercentual(10)
    assert pedido.total() == pytest.approx(46.8)

    pedido.desconto = PrimeiraCompra(50)
    assert pedido.total() == pytest.approx(26.0)

    pedido.desconto = SemDesconto()
    assert pedido.total() == pytest.approx(52.0)