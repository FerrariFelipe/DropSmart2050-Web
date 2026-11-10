
from models.encomenda import Encomenda

# Criando uma encomenda
encomenda = Encomenda(
    1,
    "BR123456789",
    "Caixa de eletrônicos",
    "2026-11-01 10:30:00",
    "RECEBIDO NA PORTARIA",
    2
)

# Exibindo os dados
print("DADOS DA ENCOMENDA")
print(encomenda.obter_detalhes())

# Atualizando o status
encomenda.atualizar_status("DISPONÍVEL PARA RETIRADA")

print("\nNOVO STATUS:")
print(encomenda.status)
