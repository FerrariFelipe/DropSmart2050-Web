
from services.usuario_service import cadastrar_usuario, fazer_login
from services.encomenda_service import atualizar_status_encomenda

from datetime import datetime

# Criar um administrador de teste
email_admin = (
    f"admin{datetime.now().strftime('%Y%m%d%H%M%S%f')}@dropsmart.com"
)

cadastrar_usuario(
    "Administrador",
    email_admin,
    "AdminTeste123",
    "ADMIN"
)

# Fazer login
usuario = fazer_login(email_admin, "AdminTeste123")

print("===== ATUALIZAÇÃO DE ENCOMENDA =====")

id_encomenda = int(input("Digite o ID da encomenda: "))

atualizar_status_encomenda(
    usuario,
    id_encomenda,
    "DISPONÍVEL PARA RETIRADA"
)

print("Status atualizado com sucesso!")
print("Nova situação: DISPONÍVEL PARA RETIRADA")
