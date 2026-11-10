
from models.administrador import Administrador
from models.morador import Morador


# Criando um administrador
admin = Administrador(
    1,
    "Carlos",
    "admin@dropsmart.com"
)

# Criando um morador
morador = Morador(
    2,
    "Joao",
    "joao@email.com"
)

# Exibindo os painéis
print(admin.exibir_painel())
print(morador.exibir_painel())

# Consultando informações
print(admin.cadastrar_encomenda())
print(morador.consultar_encomendas())

# Exibindo os perfis
print(admin.perfil)
print(morador.perfil)
