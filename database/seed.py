from pathlib import Path

from database.conexao import ConexaoBanco


BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"
DB_PATH = BASE_DIR / "delivery.db"


def seed():
    ConexaoBanco.fechar()

    conexao = ConexaoBanco.obter(str(DB_PATH))

    try:
        conexao.executescript("""
            DROP TABLE IF EXISTS historico_status;
            DROP TABLE IF EXISTS item_adicional;
            DROP TABLE IF EXISTS item_pedido;
            DROP TABLE IF EXISTS pedido;
            DROP TABLE IF EXISTS produto;
            DROP TABLE IF EXISTS cliente;
        """)

        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        conexao.executescript(schema)

        produtos = [
            ("Hambúrguer Artesanal", "hamburguer", 28.0),
            ("Pizza Mussarela", "pizza", 45.0),
            ("Refrigerante Lata", "bebida", 7.0),
            ("Pudim", "sobremesa", 12.0),
            ("Hambúrguer Bacon", "hamburguer", 35.0),
            ("Pizza Calabresa", "pizza", 48.0),
        ]

        conexao.executemany("""
            INSERT INTO produto (nome, categoria, preco)
            VALUES (?, ?, ?)
        """, produtos)

        clientes = [
            ("Maria Silva", "87900000001", "Rua A, 100", True),
            ("João Santos", "87900000002", "Rua B, 200", False),
            ("Ana Oliveira", "87900000003", "Rua C, 300", True),
        ]

        conexao.executemany("""
            INSERT INTO cliente (
                nome,
                telefone,
                endereco,
                primeira_compra
            )
            VALUES (?, ?, ?, ?)
        """, clientes)

        conexao.commit()

        print("Banco recriado com sucesso!")
        print("6 produtos cadastrados.")
        print("3 clientes cadastrados.")

    except Exception:
        conexao.rollback()
        raise

    finally:
        ConexaoBanco.fechar()


if __name__ == "__main__":
    seed()