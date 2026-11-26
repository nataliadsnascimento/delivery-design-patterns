PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS cliente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    endereco TEXT,
    primeira_compra BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco REAL NOT NULL CHECK (preco >= 0)
);

CREATE TABLE IF NOT EXISTS pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    tipo TEXT NOT NULL DEFAULT 'local',
    status TEXT NOT NULL DEFAULT 'recebido',
    subtotal REAL NOT NULL DEFAULT 0,
    frete REAL NOT NULL DEFAULT 0,
    desconto REAL NOT NULL DEFAULT 0,
    total REAL NOT NULL DEFAULT 0,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (cliente_id) REFERENCES cliente(id),

    CHECK (tipo IN ('local', 'retirada', 'entrega'))
);

CREATE TABLE IF NOT EXISTS item_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1,
    preco_unitario REAL NOT NULL,

    FOREIGN KEY (pedido_id)
        REFERENCES pedido(id) ON DELETE CASCADE,

    FOREIGN KEY (produto_id)
        REFERENCES produto(id),

    CHECK (quantidade > 0),
    CHECK (preco_unitario >= 0)
);

CREATE TABLE IF NOT EXISTS item_adicional (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_pedido_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    preco REAL NOT NULL CHECK (preco >= 0),

    FOREIGN KEY (item_pedido_id)
        REFERENCES item_pedido(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS historico_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (pedido_id)
        REFERENCES pedido(id) ON DELETE CASCADE
);