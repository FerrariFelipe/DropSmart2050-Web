
from datetime import datetime

from database.conexao import conectar
from models.encomenda import Encomenda



def cadastrar_encomenda(codigo, descricao, data_chegada, usuario_id):

    # Verificar código de rastreio
    if not codigo or not codigo.strip():
        raise ValueError("O código de rastreio é obrigatório.")

    # Verificar data de chegada
    if not data_chegada or not data_chegada.strip():
        raise ValueError("A data de chegada é obrigatória.")

    try:
        datetime.strptime(data_chegada, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(
            "Data inválida. Use o formato AAAA-MM-DD HH:MM:SS."
        )

    encomenda = Encomenda(
        None,
        codigo,
        descricao,
        data_chegada,
        "RECEBIDO NA PORTARIA",
        usuario_id
    )

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id FROM usuarios WHERE id = ? AND perfil = 'MORADOR'",
        (usuario_id,)
    )

    morador = cursor.fetchone()

    if morador is None:
        conexao.close()
        raise ValueError("Morador não encontrado.")

    cursor.execute("""
        INSERT INTO encomendas
        (codigo_rastreio, descricao, data_chegada, status, usuario_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        encomenda.codigo_rastreio,
        encomenda.descricao,
        encomenda.data_chegada,
        encomenda.status,
        encomenda.usuario_id
    ))

    encomenda_id = cursor.lastrowid
    conexao.commit()
    conexao.close()

    return encomenda_id



def listar_encomendas_por_morador(usuario_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, codigo_rastreio, descricao, data_chegada, status
        FROM encomendas
        WHERE usuario_id = ?
        ORDER BY id DESC
    """, (usuario_id,))

    encomendas = cursor.fetchall()
    conexao.close()

    return encomendas


def registrar_historico(cursor, encomenda_id, status_anterior, status_novo):

    data_alteracao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO historico_encomendas
        (encomenda_id, status_anterior, status_novo, data_alteracao)
        VALUES (?, ?, ?, ?)
    """, (
        encomenda_id,
        status_anterior,
        status_novo,
        data_alteracao
    ))


def atualizar_status_encomenda(usuario, encomenda_id, novo_status):

    if usuario.perfil != "ADMIN":
        raise PermissionError(
            "Somente o administrador pode atualizar o status."
        )

    if novo_status not in Encomenda.STATUS_VALIDOS:
        raise ValueError("Status inválido.")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT status FROM encomendas WHERE id = ?",
        (encomenda_id,)
    )

    resultado = cursor.fetchone()

    if resultado is None:
        conexao.close()
        raise ValueError("Encomenda não encontrada.")

    status_anterior = resultado[0]

    if status_anterior == novo_status:
        conexao.close()
        return

    cursor.execute("""
        UPDATE encomendas
        SET status = ?
        WHERE id = ?
    """, (novo_status, encomenda_id))

    registrar_historico(
        cursor,
        encomenda_id,
        status_anterior,
        novo_status
    )

    conexao.commit()
    conexao.close()


def solicitar_retirada(usuario, encomenda_id):

    if usuario.perfil != "MORADOR":
        raise PermissionError(
            "Somente o morador pode solicitar a retirada."
        )

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT status
        FROM encomendas
        WHERE id = ? AND usuario_id = ?
    """, (encomenda_id, usuario.id))

    resultado = cursor.fetchone()

    if resultado is None:
        conexao.close()
        raise ValueError(
            "Encomenda não encontrada ou não pertence a você."
        )

    status_anterior = resultado[0]

    if status_anterior != "DISPONÍVEL PARA RETIRADA":
        conexao.close()
        raise ValueError(
            "Encomenda não está disponível para retirada."
        )

    novo_status = "SOLICITAÇÃO DE RETIRADA"

    cursor.execute("""
        UPDATE encomendas
        SET status = ?
        WHERE id = ? AND usuario_id = ?
    """, (novo_status, encomenda_id, usuario.id))

    registrar_historico(
        cursor,
        encomenda_id,
        status_anterior,
        novo_status
    )

    conexao.commit()
    conexao.close()


def confirmar_entrega(usuario, encomenda_id):

    if usuario.perfil != "ADMIN":
        raise PermissionError(
            "Somente o administrador pode confirmar a entrega."
        )

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT status
        FROM encomendas
        WHERE id = ?
    """, (encomenda_id,))

    resultado = cursor.fetchone()

    if resultado is None:
        conexao.close()
        raise ValueError("Encomenda não encontrada.")

    status_anterior = resultado[0]

    if status_anterior != "SOLICITAÇÃO DE RETIRADA":
        conexao.close()
        raise ValueError(
            "A encomenda não possui solicitação de retirada."
        )

    novo_status = "ENTREGUE"

    cursor.execute("""
        UPDATE encomendas
        SET status = ?
        WHERE id = ?
    """, (novo_status, encomenda_id))

    registrar_historico(
        cursor,
        encomenda_id,
        status_anterior,
        novo_status
    )

    conexao.commit()
    conexao.close()


def listar_historico_encomenda(encomenda_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT status_anterior, status_novo, data_alteracao
        FROM historico_encomendas
        WHERE encomenda_id = ?
        ORDER BY id
    """, (encomenda_id,))

    historico = cursor.fetchall()
    conexao.close()

    return historico
