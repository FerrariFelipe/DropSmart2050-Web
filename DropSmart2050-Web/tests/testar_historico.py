
from services.encomenda_service import listar_historico_encomenda

print("===== HISTÓRICO DA ENCOMENDA =====")

id_encomenda = int(input("Digite o ID da encomenda: "))

historico = listar_historico_encomenda(id_encomenda)

if historico:
    for registro in historico:
        print("-------------------------")
        print("Status anterior:", registro[0])
        print("Status novo:", registro[1])
        print("Data da alteração:", registro[2])
else:
    print("Nenhum histórico registrado.")
