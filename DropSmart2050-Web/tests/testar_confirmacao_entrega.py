
from services.usuario_service import cadastrar_usuario, fazer_login
from services.encomenda_service import confirmar_entrega
from datetime import datetime

email_admin = (
    f"admin{datetime.now().strftime('%Y%m%d%H%M%S%f')}@dropsmart.com"
)

cadastrar_usuario(
    "Administrador",
    email_admin,
    "AdminTeste123",
    "ADMIN"
)

usuario = fazer_login(email_admin, "AdminTeste123")

print("===== CONFIRMAÇÃO DE ENTREGA =====")

id_encomenda = int(input("ID da encomenda: "))

try:
    confirmar_entrega(usuario, id_encomenda)

    print("\nEntrega confirmada com sucesso!")
    print("Status: ENTREGUE")

except (ValueError, PermissionError) as erro:
    print("\nNão foi possível confirmar:", erro)
