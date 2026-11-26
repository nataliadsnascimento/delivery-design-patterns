from typing import Optional

from database.conexao import ConexaoBanco
from models.cliente import Cliente


class ClienteRepository:

    def __init__(self):
        self._conexao = ConexaoBanco.obter()

    def buscar(self, id: int) -> Optional[Cliente]:

        resultado = self._conexao.execute("""
            SELECT id, nome, telefone, endereco, primeira_compra
            FROM cliente
            WHERE id = ?
        """, (id,)).fetchone()

        if resultado is None:
            return None

        return self._converter(resultado)

    def salvar(self, cliente: Cliente) -> Cliente:

        if cliente.id is None:

            cursor = self._conexao.execute("""
                INSERT INTO cliente (
                    nome, telefone, endereco, primeira_compra
                )
                VALUES (?, ?, ?, ?)
            """, (
                cliente.nome,
                cliente.telefone,
                cliente.endereco,
                cliente.primeira_compra
            ))

            cliente.id = cursor.lastrowid

        else:

            self._conexao.execute("""
                UPDATE cliente
                SET nome = ?,
                    telefone = ?,
                    endereco = ?,
                    primeira_compra = ?
                WHERE id = ?
            """, (
                cliente.nome,
                cliente.telefone,
                cliente.endereco,
                cliente.primeira_compra,
                cliente.id
            ))

        self._conexao.commit()

        return cliente

    def listar(self) -> list[Cliente]:

        resultados = self._conexao.execute("""
            SELECT id, nome, telefone, endereco, primeira_compra
            FROM cliente
            ORDER BY id
        """).fetchall()

        return [
            self._converter(resultado)
            for resultado in resultados
        ]

    @staticmethod
    def _converter(resultado) -> Cliente:

        return Cliente(
            id=resultado["id"],
            nome=resultado["nome"],
            telefone=resultado["telefone"],
            endereco=resultado["endereco"],
            primeira_compra=bool(resultado["primeira_compra"])
        )