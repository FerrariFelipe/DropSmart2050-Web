from datetime import datetime
from functools import wraps
import os

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from models.administrador import Administrador
from models.morador import Morador
from database.conexao import conectar
from services.usuario_service import fazer_login, cadastrar_usuario, listar_usuarios
from services.encomenda_service import (
    cadastrar_encomenda, listar_encomendas_por_morador,
    atualizar_status_encomenda, solicitar_retirada,
    confirmar_entrega, listar_historico_encomenda
)
from services.painel_service import consultar_todas_encomendas

app = Flask(__name__)
app.secret_key = os.environ.get('DROPSMART_SECRET', 'troque-esta-chave-em-producao')
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')

# Garante que as tabelas existam também ao iniciar a versão web pela primeira vez.
def preparar_banco():
    conexao = conectar()
    try:
        schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as arquivo:
            conexao.executescript(arquivo.read())
        conexao.commit()
    finally:
        conexao.close()

preparar_banco()

# Cria o primeiro administrador automaticamente quando as variáveis de ambiente
# estiverem configuradas no serviço de hospedagem (útil em hosts sem terminal).
def preparar_admin_inicial():
    nome = os.environ.get('DROPSMART_ADMIN_NOME', '').strip()
    email = os.environ.get('DROPSMART_ADMIN_EMAIL', '').strip()
    senha = os.environ.get('DROPSMART_ADMIN_SENHA', '')
    if not (nome and email and senha):
        return
    conexao = conectar()
    try:
        existente = conexao.execute(
            'SELECT id FROM usuarios WHERE email = ?', (email,)
        ).fetchone()
    finally:
        conexao.close()
    if existente is None:
        cadastrar_usuario(nome, email, senha, 'ADMIN')

preparar_admin_inicial()

STATUS = ['RECEBIDO NA PORTARIA', 'DISPONÍVEL PARA RETIRADA', 'SOLICITAÇÃO DE RETIRADA', 'ENTREGUE']


def usuario_atual():
    dados = session.get('usuario')
    if not dados:
        return None
    cls = Administrador if dados['perfil'] == 'ADMIN' else Morador
    return cls(dados['id'], dados['nome'], dados['email'])


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not usuario_atual():
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapper(*args, **kwargs):
        if usuario_atual().perfil != 'ADMIN':
            flash('Você não tem permissão para acessar essa área.', 'error')
            return redirect(url_for('dashboard'))
        return fn(*args, **kwargs)
    return wrapper


def buscar_resumo(usuario):
    con = conectar(); cur = con.cursor()
    if usuario.perfil == 'ADMIN':
        cur.execute('SELECT status, COUNT(*) FROM encomendas GROUP BY status')
    else:
        cur.execute('SELECT status, COUNT(*) FROM encomendas WHERE usuario_id = ? GROUP BY status', (usuario.id,))
    counts = dict(cur.fetchall())
    con.close()
    return {
        'total': sum(counts.values()),
        'recebidas': counts.get(STATUS[0], 0),
        'disponiveis': counts.get(STATUS[1], 0),
        'solicitadas': counts.get(STATUS[2], 0),
        'entregues': counts.get(STATUS[3], 0),
    }


def buscar_moradores():
    return [u for u in listar_usuarios() if u[3] == 'MORADOR']


@app.context_processor
def contexto_global():
    return {'usuario_logado': usuario_atual(), 'status_lista': STATUS}


@app.route('/')
def index():
    return redirect(url_for('dashboard') if usuario_atual() else url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if usuario_atual():
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        usuario = fazer_login(email, senha)
        if usuario:
            session.clear()
            session['usuario'] = {'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email, 'perfil': usuario.perfil}
            flash(f'Bem-vindo(a), {usuario.nome.split()[0]}!', 'success')
            return redirect(url_for('dashboard'))
        flash('E-mail ou senha incorretos.', 'error')
    return render_template('login.html')


@app.route('/sair')
def logout():
    session.clear(); flash('Você saiu do sistema.', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    usuario = usuario_atual()
    if usuario.perfil == 'ADMIN':
        encomendas = consultar_todas_encomendas()
    else:
        encomendas = [(*e, usuario.nome) for e in listar_encomendas_por_morador(usuario.id)]
    return render_template('dashboard.html', resumo=buscar_resumo(usuario), encomendas=encomendas[:8], pagina='dashboard')


@app.route('/encomendas')
@login_required
def encomendas():
    usuario = usuario_atual()
    if usuario.perfil == 'ADMIN':
        registros = consultar_todas_encomendas()
    else:
        registros = [(*e, usuario.nome) for e in listar_encomendas_por_morador(usuario.id)]
    filtro = request.args.get('status', '')
    busca = request.args.get('q', '').strip().lower()
    if filtro: registros = [e for e in registros if e[4] == filtro]
    if busca: registros = [e for e in registros if busca in str(e[1]).lower() or busca in str(e[2]).lower() or busca in str(e[5]).lower()]
    return render_template('encomendas.html', encomendas=registros, pagina='encomendas', filtro=filtro, busca=request.args.get('q',''))


@app.route('/encomendas/nova', methods=['GET', 'POST'])
@admin_required
def nova_encomenda():
    moradores = buscar_moradores()
    if request.method == 'POST':
        try:
            data = datetime.strptime(request.form.get('data_chegada',''), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
            novo_id = cadastrar_encomenda(request.form.get('codigo',''), request.form.get('descricao',''), data, int(request.form.get('morador_id','0')))
            flash(f'Encomenda #{novo_id} cadastrada com sucesso!', 'success')
            return redirect(url_for('encomendas'))
        except (ValueError, TypeError) as erro:
            flash(str(erro), 'error')
    return render_template('nova_encomenda.html', moradores=moradores, pagina='nova')


@app.post('/encomendas/<int:encomenda_id>/acao')
@login_required
def acao_encomenda(encomenda_id):
    usuario = usuario_atual(); acao = request.form.get('acao')
    try:
        if acao == 'liberar' and usuario.perfil == 'ADMIN':
            atualizar_status_encomenda(usuario, encomenda_id, STATUS[1]); flash('Encomenda liberada para retirada.', 'success')
        elif acao == 'solicitar' and usuario.perfil == 'MORADOR':
            solicitar_retirada(usuario, encomenda_id); flash('Solicitação enviada à portaria.', 'success')
        elif acao == 'entregar' and usuario.perfil == 'ADMIN':
            confirmar_entrega(usuario, encomenda_id); flash('Entrega confirmada com sucesso.', 'success')
        else:
            abort(403)
    except (ValueError, PermissionError) as erro:
        flash(str(erro), 'error')
    return redirect(request.referrer or url_for('encomendas'))


@app.route('/historico')
@login_required
def historico():
    usuario = usuario_atual()
    if usuario.perfil == 'ADMIN':
        registros = consultar_todas_encomendas()
    else:
        registros = [(*e, usuario.nome) for e in listar_encomendas_por_morador(usuario.id)]
    selecionada = request.args.get('id', type=int)
    if selecionada and not any(e[0] == selecionada for e in registros): abort(403)
    eventos = listar_historico_encomenda(selecionada) if selecionada else []
    encomenda = next((e for e in registros if e[0] == selecionada), None)
    return render_template('historico.html', encomendas=registros, eventos=eventos, selecionada=selecionada, encomenda=encomenda, pagina='historico')


@app.route('/moradores', methods=['GET', 'POST'])
@admin_required
def moradores():
    if request.method == 'POST':
        try:
            novo_id = cadastrar_usuario(request.form.get('nome',''), request.form.get('email',''), request.form.get('senha',''), 'MORADOR')
            flash(f'Morador cadastrado com sucesso! ID {novo_id}.', 'success')
            return redirect(url_for('moradores'))
        except Exception as erro:
            flash(str(erro), 'error')
    return render_template('moradores.html', moradores=buscar_moradores(), pagina='moradores')


@app.errorhandler(403)
def proibido(_):
    flash('Ação não autorizada para seu perfil.', 'error')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
