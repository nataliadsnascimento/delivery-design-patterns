import sqlite3

import pytest

from database.conexao import ConexaoBanco

@pytest.fixture(autouse=True)
def limpar_conexao():
    ConexaoBanco.fechar()
    yield
    ConexaoBanco.fechar()


def test_conexao_unica():
    conexao1 = ConexaoBanco.obter(":memory:")
    conexao2 = ConexaoBanco.obter(":memory:")

    assert conexao1 is conexao2


def test_row_factory():
    conexao = ConexaoBanco.obter(":memory:")

    assert conexao.row_factory is sqlite3.Row

    resultado = conexao.execute(
        "SELECT 1 AS id"
    ).fetchone()

    assert resultado["id"] == 1


def test_foreign_keys():
    conexao = ConexaoBanco.obter(":memory:")

    resultado = conexao.execute(
        "PRAGMA foreign_keys"
    ).fetchone()

    assert resultado[0] == 1


def test_banco_em_memoria():
    conexao = ConexaoBanco.obter(":memory:")

    conexao.execute("""
        CREATE TABLE clientes (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL
        )
    """)

    conexao.execute(
        "INSERT INTO clientes (nome) VALUES (?)",
        ("Maria",)
    )

    resultado = conexao.execute(
        "SELECT * FROM clientes"
    ).fetchone()

    assert resultado["nome"] == "Maria"