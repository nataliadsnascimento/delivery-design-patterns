import sqlite3

class ConexaoBanco:

    _conexao = None

    @classmethod
    def obter(cls, caminho: str = "database/delivery.db") -> sqlite3.Connection:

        if cls._conexao is None:
            cls._conexao = sqlite3.connect(caminho)

            cls._conexao.row_factory = sqlite3.Row
            cls._conexao.execute("PRAGMA foreign_keys = ON")

        return cls._conexao

    @classmethod
    def fechar(cls) -> None:
        if cls._conexao is not None:
            cls._conexao.close()
            cls._conexao = None