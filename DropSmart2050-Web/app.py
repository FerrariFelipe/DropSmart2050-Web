
from database.conexao import conectar
from services.usuario_service import fazer_login
from services.painel_service import abrir_painel


def criar_banco():

    conexao = conectar()

    try:
        with open(
            "database/schema.sql",
            "r",
            encoding="utf-8"
        ) as arquivo:

            script_sql = arquivo.read()

        conexao.executescript(script_sql)
        conexao.commit()

        print("Banco de dados preparado com sucesso!")

    finally:
        conexao.close()


def iniciar_sistema():

    criar_banco()

    while True:

        print("\n================================")
        print("        DROPSMART 2050")
        print("================================")
        print("1 - Entrar")
        print("0 - Sair")
        print("--------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            email = input("E-mail: ")
            senha = input("Senha: ")

            usuario = fazer_login(email, senha)

            if usuario:

                print("\nLogin realizado com sucesso!")

                abrir_painel(usuario)

            else:

                print("\nE-mail ou senha incorretos.")

        elif opcao == "0":

            print("\nObrigado por utilizar o DropSmart 2050!")
            break

        else:

            print("\nOpção inválida.")


if __name__ == "__main__":
    iniciar_sistema()
