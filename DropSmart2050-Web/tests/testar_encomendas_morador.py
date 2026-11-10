from services.usuario_service import fazer_login
from services.encomenda_service import listar_encomendas_por_morador

print("===== ENCOMENDAS DO MORADOR =====")

email = input("E-mail do morador: ")
senha = input("Senha: ")

usuario = fazer_login(email, senha)

if usuario and usuario["perfil"] == "MORADOR":

    encomendas = listar_encomendas_por_morador(usuario["id"])

    if encomendas:
        for encomenda in encomendas:
            print("------------------------------")
            print(f"ID da encomenda: {encomenda[0]}")
            print(f"Código de rastreio: {encomenda[1]}")
            print(f"Descrição: {encomenda[2]}")
            print(f"Data de chegada: {encomenda[3]}")
            print(f"Status: {encomenda[4]}")
    else:
        print("Nenhuma encomenda encontrada.")

else:
    print("Login inválido ou usuário não é morador.")
