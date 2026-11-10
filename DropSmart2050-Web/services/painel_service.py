

from database.conexao import conectar

from services.encomenda_service import (
    cadastrar_encomenda,
    listar_encomendas_por_morador,
    atualizar_status_encomenda,
    solicitar_retirada,
    confirmar_entrega,
    listar_historico_encomenda
)


def consultar_todas_encomendas():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            e.id,
            e.codigo_rastreio,
            e.descricao,
            e.data_chegada,
            e.status,
            u.nome
        FROM encomendas e
        INNER JOIN usuarios u ON e.usuario_id = u.id
        ORDER BY e.id DESC
    """)

    encomendas = cursor.fetchall()
    conexao.close()

    return encomendas


def menu_administrador(usuario):

    while True:
        print("\n========== DROPSMART 2050 ==========")
        print("PAINEL DO ADMINISTRADOR")
        print("Bem-vindo(a),", usuario.nome)
        print("------------------------------------")
        print("1 - Cadastrar encomenda")
        print("2 - Consultar encomendas")
        print("3 - Liberar encomenda para retirada")
        print("4 - Confirmar entrega")
        print("5 - Consultar histórico")
        print("0 - Sair")
        print("------------------------------------")

        opcao = input("Escolha uma opção: ")

        try:

            if opcao == "1":

                codigo = input("Código de rastreio: ")
                descricao = input("Descrição: ")
                data = input("Data de chegada: ")
                usuario_id = int(input("ID do morador: "))

                encomenda_id = cadastrar_encomenda(
                    codigo,
                    descricao,
                    data,
                    usuario_id
                )

                print("Encomenda cadastrada com sucesso!")
                print("ID da encomenda:", encomenda_id)

            elif opcao == "2":

                encomendas = consultar_todas_encomendas()

                if not encomendas:
                    print("Nenhuma encomenda cadastrada.")

                for e in encomendas:
                    print("--------------------------------")
                    print("ID:", e[0])
                    print("Rastreio:", e[1])
                    print("Descrição:", e[2])
                    print("Chegada:", e[3])
                    print("Status:", e[4])
                    print("Morador:", e[5])

            elif opcao == "3":

                encomenda_id = int(
                    input("ID da encomenda: ")
                )

                atualizar_status_encomenda(
                    usuario,
                    encomenda_id,
                    "DISPONÍVEL PARA RETIRADA"
                )

                print("Encomenda liberada para retirada!")

            elif opcao == "4":

                encomenda_id = int(
                    input("ID da encomenda: ")
                )

                confirmar_entrega(usuario, encomenda_id)

                print("Entrega confirmada com sucesso!")

            elif opcao == "5":

                encomenda_id = int(
                    input("ID da encomenda: ")
                )

                historico = listar_historico_encomenda(
                    encomenda_id
                )

                if not historico:
                    print("Nenhum histórico encontrado.")

                for h in historico:
                    print("--------------------------------")
                    print("Status anterior:", h[0])
                    print("Status novo:", h[1])
                    print("Data:", h[2])

            elif opcao == "0":

                print("Saindo do painel do administrador...")
                break

            else:
                print("Opção inválida.")

        except (ValueError, PermissionError) as erro:
            print("Não foi possível realizar a operação:", erro)


def menu_morador(usuario):

    while True:
        print("\n========== DROPSMART 2050 ==========")
        print("PAINEL DO MORADOR")
        print("Bem-vindo(a),", usuario.nome)
        print("------------------------------------")
        print("1 - Consultar minhas encomendas")
        print("2 - Solicitar retirada")
        print("3 - Consultar histórico")
        print("0 - Sair")
        print("------------------------------------")

        opcao = input("Escolha uma opção: ")

        try:

            if opcao == "1":

                encomendas = listar_encomendas_por_morador(
                    usuario.id
                )

                if not encomendas:
                    print("Você não possui encomendas.")

                for e in encomendas:
                    print("--------------------------------")
                    print("ID:", e[0])
                    print("Rastreio:", e[1])
                    print("Descrição:", e[2])
                    print("Chegada:", e[3])
                    print("Status:", e[4])

            elif opcao == "2":

                encomenda_id = int(
                    input("ID da encomenda: ")
                )

                solicitar_retirada(
                    usuario,
                    encomenda_id
                )

                print("Solicitação realizada com sucesso!")

            elif opcao == "3":

                encomenda_id = int(
                    input("ID da encomenda: ")
                )

                minhas_encomendas = listar_encomendas_por_morador(
                    usuario.id
                )

                ids_validos = [e[0] for e in minhas_encomendas]

                if encomenda_id not in ids_validos:
                    print("Essa encomenda não pertence a você.")
                    continue

                historico = listar_historico_encomenda(
                    encomenda_id
                )

                if not historico:
                    print("Nenhum histórico encontrado.")

                for h in historico:
                    print("--------------------------------")
                    print("Status anterior:", h[0])
                    print("Status novo:", h[1])
                    print("Data:", h[2])

            elif opcao == "0":

                print("Saindo do painel do morador...")
                break

            else:
                print("Opção inválida.")

        except (ValueError, PermissionError) as erro:
            print("Não foi possível realizar a operação:", erro)


def abrir_painel(usuario):

    if usuario.perfil == "ADMIN":
        menu_administrador(usuario)

    elif usuario.perfil == "MORADOR":
        menu_morador(usuario)

    else:
        print("Perfil não reconhecido.")
