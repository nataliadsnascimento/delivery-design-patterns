from pathlib import Path

import pytest

from database.conexao import ConexaoBanco
from models.cliente import Cliente
from repositories.cliente_repository import ClienteRepository


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "database"
    / "schema.sql"
)


@pytest.fixture
def repository():

    ConexaoBanco.fechar()

    conexao = ConexaoBanco.obter(":memory:")

    try:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        conexao.executescript(schema)

        yield ClienteRepository()

    finally:
        ConexaoBanco.fechar()


def test_salvar_cliente(repository):

    cliente = Cliente(
        nome="Maria Silva",
        telefone="87900000001",
        endereco="Rua A, 100"
    )

    resultado = repository.salvar(cliente)

    assert resultado.id is not None
    assert resultado.nome == "Maria Silva"
    assert resultado.primeira_compra is True


def test_buscar_cliente(repository):

    cliente = Cliente(
        nome="João Santos",
        telefone="87900000002"
    )

    repository.salvar(cliente)

    resultado = repository.buscar(cliente.id)

    assert resultado is not None
    assert resultado.id == cliente.id
    assert resultado.nome == "João Santos"
    assert resultado.telefone == "87900000002"


def test_buscar_cliente_inexistente(repository):

    resultado = repository.buscar(999)

    assert resultado is None


def test_listar_clientes(repository):

    repository.salvar(
        Cliente(
            nome="Maria",
            telefone="87900000001"
        )
    )

    repository.salvar(
        Cliente(
            nome="João",
            telefone="87900000002"
        )
    )

    clientes = repository.listar()

    assert len(clientes) == 2
    assert clientes[0].nome == "Maria"
    assert clientes[1].nome == "João"


def test_listar_clientes_vazio(repository):

    assert repository.listar() == []


def test_atualizar_cliente(repository):

    cliente = Cliente(
        nome="Ana",
        telefone="87900000003"
    )

    repository.salvar(cliente)

    cliente.nome = "Ana Oliveira"
    cliente.primeira_compra = False

    repository.salvar(cliente)

    resultado = repository.buscar(cliente.id)

    assert resultado.nome == "Ana Oliveira"
    assert resultado.primeira_compra is False
    assert len(repository.listar()) == 1


def test_consulta_parametrizada(repository):

    nome = "Cliente ' Teste"

    cliente = Cliente(
        nome=nome,
        telefone="87900000004"
    )

    repository.salvar(cliente)

    resultado = repository.buscar(cliente.id)

    assert resultado.nome == nome