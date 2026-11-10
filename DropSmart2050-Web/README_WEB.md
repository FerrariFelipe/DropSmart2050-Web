# DropSmart 2050 — Interface Web

A interface web foi adicionada preservando os models, services e o SQLite existentes. O terminal original continua disponível em `app.py`; a versão web inicia por `web_app.py`.

## Executar

1. Abra o terminal na pasta do projeto.
2. Crie um ambiente virtual (recomendado): `python -m venv .venv`
3. Ative-o: Windows PowerShell `.venv\Scripts\Activate.ps1` ou CMD `.venv\Scripts\activate.bat`.
4. Instale: `pip install -r requirements.txt`
5. Inicie: `python web_app.py`
6. Acesse `http://127.0.0.1:5000`.

As tabelas do SQLite são preparadas automaticamente quando a aplicação web é iniciada. Para criar o primeiro acesso administrativo, execute `python criar_admin.py` e siga as instruções no terminal. Não existe senha padrão embutida.

## Funcionalidades da interface
- Login com a autenticação PBKDF2 existente e sessão Flask.
- Dashboard com indicadores e encomendas recentes.
- Listagem com busca e filtro por status.
- Cadastro de encomendas (administrador).
- Liberação e confirmação de entrega (administrador).
- Solicitação de retirada (morador).
- Histórico por encomenda com validação de propriedade.
- Cadastro e listagem de moradores (administrador).

## Observações
- `app.py` permanece como aplicação de terminal.
- Para produção, defina `DROPSMART_SECRET` com uma chave forte, desative `debug=True` e use HTTPS.
- A interface usa Google Fonts e Lucide via CDN; sem internet, o sistema continua utilizável, mas fontes/ícones podem não carregar.
