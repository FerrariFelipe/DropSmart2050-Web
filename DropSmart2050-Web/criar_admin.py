from getpass import getpass
from services.usuario_service import cadastrar_usuario

"""Cria o primeiro administrador do DropSmart 2050."""

nome = input("Nome do administrador: ").strip()
email = input("E-mail: ").strip()
senha = getpass("Senha (mínimo 6 caracteres): ")
confirmacao = getpass("Confirme a senha: ")
if senha != confirmacao:
    raise SystemExit("As senhas não coincidem.")
try:
    usuario_id = cadastrar_usuario(nome, email, senha, "ADMIN")
    print(f"Administrador criado com sucesso! ID: {usuario_id}")
except Exception as erro:
    raise SystemExit(f"Não foi possível criar o administrador: {erro}")
