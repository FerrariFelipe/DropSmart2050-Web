
from services.usuario_service import fazer_login
from services.encomenda_service import solicitar_retirada

print("===== SOLICITAÇÃO DE RETIRADA =====")

email = input("E-mail do morador: ")
senha = input("Senha: ")

usuario = fazer_login(email, senha)

if usuario is None:
    print("E-mail ou senha incorretos.")

else:
    try:
        id_encomenda = int(input("ID da encomenda: "))

        solicitar_retirada(usuario, id_encomenda)

        print("\nSolicitação realizada com sucesso!")
        print("Status: SOLICITAÇÃO DE RETIRADA")

    except (ValueError, PermissionError) as erro:
        print("\nNão foi possível solicitar:", erro)
