
class Encomenda:

    STATUS_VALIDOS = [
        "RECEBIDO NA PORTARIA",
        "DISPONÍVEL PARA RETIRADA",
        "SOLICITAÇÃO DE RETIRADA",
        "ENTREGUE"
    ]

    def __init__(
        self,
        id,
        codigo_rastreio,
        descricao,
        data_chegada,
        status,
        usuario_id
    ):
        if not codigo_rastreio:
            raise ValueError("O código de rastreio é obrigatório.")

        if not descricao or not descricao.strip():
            raise ValueError("A descrição da encomenda é obrigatória.")

        if status not in self.STATUS_VALIDOS:
            raise ValueError("Status de encomenda inválido.")

        self.id = id
        self.codigo_rastreio = codigo_rastreio
        self.descricao = descricao
        self.data_chegada = data_chegada
        self.status = status
        self.usuario_id = usuario_id

    def atualizar_status(self, novo_status):
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError("Status inválido.")

        self.status = novo_status

    def obter_detalhes(self):
        return {
            "id": self.id,
            "codigo_rastreio": self.codigo_rastreio,
            "descricao": self.descricao,
            "data_chegada": self.data_chegada,
            "status": self.status,
            "usuario_id": self.usuario_id
        }
