from pathlib import Path

import pytest

from database.conexao import ConexaoBanco


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "database"
    / "schema.sql"
)


@pytest.fixture
def conexao():
    ConexaoBanco.fechar()

    banco = ConexaoBanco.obter(":memory:")

    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    banco.executescript(schema)

    yield banco

    ConexaoBanco.fechar()


def test_schema_cria_seis_tabelas(conexao):
    resultado = conexao.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """).fetchall()

    tabelas = {linha["name"] for linha in resultado}

    tabelas_esperadas = {
        "cliente",
        "produto",
        "pedido",
        "item_pedido",
        "item_adicional",
        "historico_status",
    }

    assert tabelas == tabelas_esperadas
    assert len(tabelas) == 6