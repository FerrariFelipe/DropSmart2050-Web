
from services.usuario_service import fazer_login
from services.painel_service import abrir_painel

email = input("Digite seu e-mail: ")
senha = input("Digite sua senha: ")

usuario = fazer_login(email, senha)

if usuario:
    abrir_painel(usuario)
else:
    print("E-mail ou senha incorretos.")
