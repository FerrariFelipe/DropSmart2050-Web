from models.administrador import Administrador
from models.morador import Morador

import hashlib
import secrets


from database.conexao import conectar


def gerar_hash_senha(senha):
    salt = secrets.token_hex(16)

    hash_senha = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()

    return f"{salt}${hash_senha}"



def cadastrar_usuario(nome, email, senha, perfil):

    if perfil not in ("ADMIN", "MORADOR"):
        raise ValueError("Perfil inválido.")

    if not nome or not nome.strip():
        raise ValueError("O nome é obrigatório.")

    if not email or not email.strip():
        raise ValueError("O e-mail é obrigatório.")

    if "@" not in email or "." not in email:
        raise ValueError("Digite um e-mail válido.")

    if not senha:
        raise ValueError("A senha é obrigatória.")

    if len(senha) < 6:
        raise ValueError("A senha deve ter pelo menos 6 caracteres.")

    senha_protegida = gerar_hash_senha(senha)

    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, perfil)
            VALUES (?, ?, ?, ?)
        """, (nome.strip(), email.strip(), senha_protegida, perfil))

        conexao.commit()

        return cursor.lastrowid

    finally:
        conexao.close()


def listar_usuarios():

    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, email, perfil
            FROM usuarios
            ORDER BY id
        """)

        usuarios = cursor.fetchall()

        return usuarios

    finally:
        conexao.close()

def verificar_senha(senha_digitada, senha_salva):

    salt, hash_original = senha_salva.split("$")

    hash_digitado = hashlib.pbkdf2_hmac(
        "sha256",
        senha_digitada.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()

    return secrets.compare_digest(hash_original, hash_digitado)


def fazer_login(email, senha):

    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, email, senha, perfil
            FROM usuarios
            WHERE email = ?
        """, (email,))

        usuario = cursor.fetchone()

        if usuario is None:
            return None

        if verificar_senha(senha, usuario[3]):

            if usuario[4] == "ADMIN":
                return Administrador(
                    usuario[0],
                    usuario[1],
                    usuario[2]
                )

            elif usuario[4] == "MORADOR":
                return Morador(
                    usuario[0],
                    usuario[1],
                    usuario[2]
                )

        return None

    finally:
        conexao.close()
