
from services.usuario_service import listar_usuarios

usuarios = listar_usuarios()

print("\n===== USUÁRIOS CADASTRADOS =====")

if usuarios:
    for usuario in usuarios:
        print("-------------------------")
        print("ID:", usuario[0])
        print("Nome:", usuario[1])
        print("E-mail:", usuario[2])
        print("Perfil:", usuario[3])
else:
    print("Nenhum usuário cadastrado.")
