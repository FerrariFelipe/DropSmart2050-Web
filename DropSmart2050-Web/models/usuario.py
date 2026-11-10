
from abc import ABC, abstractmethod


class Usuario(ABC):

    def __init__(self, id, nome, email, perfil):
        self._id = id
        self._nome = nome
        self._email = email
        self._perfil = perfil

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email

    @property
    def perfil(self):
        return self._perfil

    @abstractmethod
    def exibir_painel(self):
        pass
