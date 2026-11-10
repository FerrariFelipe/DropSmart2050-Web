
import sqlite3
from pathlib import Path

# Localiza a pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho do banco de dados
DATABASE = BASE_DIR / "database.db"


def conectar():
    conexao = sqlite3.connect(DATABASE)

    # Ativa a integridade das chaves estrangeiras
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao
