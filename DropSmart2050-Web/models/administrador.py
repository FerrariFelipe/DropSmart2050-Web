
from models.usuario import Usuario


class Administrador(Usuario):

    def __init__(self, id, nome, email):
        super().__init__(id, nome, email, "ADMIN")

    def exibir_painel(self):
        return "Painel do Administrador"

    def cadastrar_encomenda(self):
        return "Cadastro de encomendas"

    def consultar_relatorios(self):
        return "Relatórios do condomínio"
