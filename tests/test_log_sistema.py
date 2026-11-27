import sqlite3
from pathlib import Path

import pytest

from database.conexao import ConexaoBanco
from models.cliente import Cliente
from models.pedido import Pedido
from observers.observador import LogSistema, NotificadorCliente
from states.estados_pedido import TransicaoInvalidaError

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "database" / "schema.sql"


@pytest.fixture
def banco():
    ConexaoBanco.fechar()
    conexao = ConexaoBanco.obter(":memory:")
    try:
        conexao.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        yield conexao
    finally:
        ConexaoBanco.fechar()


def _criar_pedido(banco, nome="Maria Silva"):
    banco.execute(
        "INSERT INTO cliente (nome, telefone, endereco) VALUES (?, ?, ?)",
        (nome, "81 99999-0000", "Rua A, 1"),
    )
    cliente_id = banco.execute("SELECT last_insert_rowid()").fetchone()[0]
    cursor = banco.execute(
        "INSERT INTO pedido (cliente_id, tipo) VALUES (?, 'entrega')", (cliente_id,)
    )
    banco.commit()

    pedido = Pedido(Cliente(nome=nome, telefone="81 99999-0000"), tipo="entrega")
    pedido.id = cursor.lastrowid
    return pedido


def _historico(banco, pedido_id):
    return banco.execute(
        "SELECT pedido_id, status, criado_em FROM historico_status "
        "WHERE pedido_id = ? ORDER BY id",
        (pedido_id,),
    ).fetchall()


def test_grava_pedido_id_status_e_data_hora(banco):
    pedido = _criar_pedido(banco)
    pedido.adicionar_observador(LogSistema())

    pedido.avancar()

    linhas = _historico(banco, pedido.id)
    assert len(linhas) == 1
    assert linhas[0]["pedido_id"] == pedido.id
    assert linhas[0]["status"] == "preparando"
    assert linhas[0]["criado_em"] is not None


def test_grava_uma_linha_por_mudanca_na_ordem(banco):
    pedido = _criar_pedido(banco)
    pedido.adicionar_observador(LogSistema())

    pedido.avancar()
    pedido.avancar()
    pedido.avancar()

    status = [linha["status"] for linha in _historico(banco, pedido.id)]
    assert status == ["preparando", "a_caminho", "entregue"]


def test_cancelamento_tambem_e_gravado(banco):
    pedido = _criar_pedido(banco)
    pedido.adicionar_observador(LogSistema())

    pedido.cancelar()

    assert [l["status"] for l in _historico(banco, pedido.id)] == ["cancelado"]


def test_transicao_invalida_nao_grava(banco):
    pedido = _criar_pedido(banco)
    pedido.adicionar_observador(LogSistema())
    pedido.cancelar()

    with pytest.raises(TransicaoInvalidaError):
        pedido.avancar()

    assert len(_historico(banco, pedido.id)) == 1  


def test_cada_pedido_tem_o_proprio_historico(banco):
    p1 = _criar_pedido(banco, "Maria")
    p2 = _criar_pedido(banco, "João")
    log = LogSistema()
    p1.adicionar_observador(log)
    p2.adicionar_observador(log)

    p1.avancar()
    p2.avancar()
    p2.avancar()

    assert len(_historico(banco, p1.id)) == 1
    assert len(_historico(banco, p2.id)) == 2


def test_usa_a_conexao_singleton(banco):
    pedido = _criar_pedido(banco)
    pedido.adicionar_observador(LogSistema())

    pedido.avancar()
    assert ConexaoBanco.obter() is banco
    assert len(_historico(ConexaoBanco.obter(), pedido.id)) == 1


def test_pedido_sem_id_da_erro_claro(banco):
    pedido = Pedido(Cliente(nome="Ana", telefone="1"))  

    with pytest.raises(ValueError):
        LogSistema().atualizar(pedido, "preparando")


def test_pedido_que_nao_existe_no_banco_e_recusado(banco):
    pedido = Pedido(Cliente(nome="Ana", telefone="1"))
    pedido.id = 999  

    with pytest.raises(sqlite3.IntegrityError):
        LogSistema().atualizar(pedido, "preparando")


def test_consulta_parametrizada_protege_de_sql_injection(banco):
    pedido = _criar_pedido(banco)
    texto_malicioso = "x'); DROP TABLE historico_status; --"

    LogSistema().atualizar(pedido, texto_malicioso)

    linhas = _historico(banco, pedido.id) 
    assert linhas[0]["status"] == texto_malicioso


def test_funciona_junto_com_outros_observadores(banco, capsys):
    pedido = _criar_pedido(banco)
    pedido.adicionar_observador(NotificadorCliente())
    pedido.adicionar_observador(LogSistema())

    pedido.avancar()

    assert "Preparando" in capsys.readouterr().out
    assert len(_historico(banco, pedido.id)) == 1