from typing import Optional

from database.conexao import ConexaoBanco
from models.item import Item
from models.itens import Bebida, Hamburguer, Pizza, Sobremesa


class ProdutoRepository:

    _CLASSES = {
        "hamburguer": Hamburguer,
        "pizza": Pizza,
        "bebida": Bebida,
        "sobremesa": Sobremesa,
    }

    def __init__(self):
        self._conexao = ConexaoBanco.obter()

    def buscar(self, id: int) -> Optional[Item]:

        resultado = self._conexao.execute("""
            SELECT id, nome, categoria, preco
            FROM produto
            WHERE id = ?
        """, (id,)).fetchone()

        if resultado is None:
            return None

        return self._converter(resultado)

    def listar_cardapio(self) -> list[Item]:

        resultados = self._conexao.execute("""
            SELECT id, nome, categoria, preco
            FROM produto
            ORDER BY id
        """).fetchall()

        return [
            self._converter(resultado)
            for resultado in resultados
        ]

    @classmethod
    def _converter(cls, resultado) -> Item:

        categoria = resultado["categoria"]
        classe = cls._CLASSES.get(categoria)

        if classe is None:
            raise ValueError(f"Categoria de produto desconhecida: {categoria}")

        return classe(
            nome=resultado["nome"],
            preco_base=resultado["preco"]
        )