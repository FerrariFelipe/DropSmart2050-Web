
from services.usuario_service import fazer_login

email = input("Digite seu e-mail: ")
senha = input("Digite sua senha: ")

usuario = fazer_login(email, senha)

if usuario:
    print("\nLOGIN REALIZADO COM SUCESSO!")
    print("Nome:", usuario["nome"])
    print("Perfil:", usuario["perfil"])
else:
    print("\nE-mail ou senha incorretos.")
