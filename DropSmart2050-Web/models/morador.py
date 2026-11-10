
from models.usuario import Usuario


class Morador(Usuario):

    def __init__(self, id, nome, email):
        super().__init__(id, nome, email, "MORADOR")

    def exibir_painel(self):
        return "Painel do Morador"

    def consultar_encomendas(self):
        return "Consulta das próprias encomendas"

    def solicitar_retirada(self):
        return "Solicitação de retirada"
