from pathlib import Path

import pytest

from database.conexao import ConexaoBanco
from models.itens import Bebida, Hamburguer, Pizza, Sobremesa
from repositories.produto_repository import ProdutoRepository


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "database"
    / "schema.sql"
)


@pytest.fixture
def conexao():

    ConexaoBanco.fechar()

    conexao = ConexaoBanco.obter(":memory:")

    try:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        conexao.executescript(schema)

        yield conexao

    finally:
        ConexaoBanco.fechar()


@pytest.fixture
def repository(conexao):

    conexao.executemany("""
        INSERT INTO produto (nome, categoria, preco)
        VALUES (?, ?, ?)
    """, [
        ("Hambúrguer Artesanal", "hamburguer", 28.0),
        ("Pizza Mussarela", "pizza", 45.0),
        ("Refrigerante Lata", "bebida", 7.0),
        ("Pudim", "sobremesa", 12.0),
    ])
    conexao.commit()

    return ProdutoRepository()


@pytest.mark.parametrize("id, classe", [
    (1, Hamburguer),
    (2, Pizza),
    (3, Bebida),
    (4, Sobremesa),
])
def test_buscar_retorna_classe_concreta(repository, id, classe):

    resultado = repository.buscar(id)

    assert isinstance(resultado, classe)


def test_buscar_produto(repository):

    resultado = repository.buscar(2)

    assert resultado is not None
    assert resultado.descricao() == "Pizza Mussarela"
    assert resultado.preco() == 45.0


def test_buscar_produto_inexistente(repository):
    assert repository.buscar(999) is None


def test_listar_cardapio(repository):
    cardapio = repository.listar_cardapio()

    assert len(cardapio) == 4
    assert [type(item) for item in cardapio] == [
        Hamburguer, Pizza, Bebida, Sobremesa
    ]
    assert cardapio[0].descricao() == "Hambúrguer Artesanal"
    assert cardapio[3].preco() == 12.0


def test_listar_cardapio_vazio(conexao):
    assert ProdutoRepository().listar_cardapio() == []


def test_categoria_desconhecida(conexao):
    conexao.execute("""
        INSERT INTO produto (nome, categoria, preco)
        VALUES ('Sorvete', 'categoria_inexistente', 10.0)
    """)
    conexao.commit()

    with pytest.raises(ValueError):
        ProdutoRepository().buscar(1)


def test_consulta_parametrizada(repository):
    assert repository.buscar("1 OR 1=1") is None