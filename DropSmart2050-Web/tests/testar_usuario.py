
from datetime import datetime

from services.usuario_service import cadastrar_usuario

email_teste = (
    f"teste{datetime.now().strftime('%Y%m%d%H%M%S%f')}@email.com"
)

id_usuario = cadastrar_usuario(
    "João Silva",
    email_teste,
    "SenhaTeste123",
    "MORADOR"
)

print("Usuário cadastrado com sucesso!")
print("ID do usuário:", id_usuario)
print("E-mail:", email_teste)
