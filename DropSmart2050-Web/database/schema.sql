
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    perfil TEXT NOT NULL
        CHECK (perfil IN ('ADMIN', 'MORADOR'))
);

CREATE TABLE IF NOT EXISTS encomendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_rastreio TEXT NOT NULL,
    descricao TEXT,
    data_chegada TEXT NOT NULL,
    status TEXT NOT NULL,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS historico_encomendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    encomenda_id INTEGER NOT NULL,
    status_anterior TEXT,
    status_novo TEXT NOT NULL,
    data_alteracao TEXT NOT NULL,
    FOREIGN KEY (encomenda_id)
        REFERENCES encomendas(id)
);
