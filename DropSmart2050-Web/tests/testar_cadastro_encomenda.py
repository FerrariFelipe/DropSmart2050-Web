
from services.encomenda_service import cadastrar_encomenda

print("===== CADASTRO DE ENCOMENDA =====")

codigo = input("Código de rastreio: ")
descricao = input("Descrição: ")
data_chegada = input("Data de chegada (AAAA-MM-DD HH:MM:SS): ")
usuario_id = int(input("ID do morador: "))

id_encomenda = cadastrar_encomenda(
    codigo,
    descricao,
    data_chegada,
    usuario_id
)

print("\nEncomenda cadastrada com sucesso!")
print("ID da encomenda:", id_encomenda)
