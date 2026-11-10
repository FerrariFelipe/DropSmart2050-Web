
from database.conexao import conectar

conexao = conectar()

print("Conexão com SQLite realizada com sucesso!")

conexao.close()
