from models.administrador import Administrador
from models.morador import Morador


admin = Administrador(
    1,
    "Administrador Principal",
    "admin@dropsmart.com"
)

morador = Morador(
    2,
    "João Silva",
    "joao@dropsmart.com"
)

usuarios = [admin, morador]

for usuario in usuarios:
    print(usuario.exibir_painel())
from models.usuario import Usuario

try:
    usuario = Usuario(1, "Teste", "teste@email.com", "ADMIN")
except TypeError:
    print("Teste aprovado: não é possível criar Usuario diretamente.")