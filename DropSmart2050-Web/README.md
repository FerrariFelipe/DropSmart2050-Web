# 📦 DropSmart 2050

**Sistema Inteligente de Gestão de Encomendas Residenciais**

Projeto acadêmico desenvolvido para a **ExpoTech 2026.2 – Missão 2050: Smart Home & Tecnologias do Futuro**.

## 🎯 Sobre o projeto

O DropSmart 2050 é um sistema desenvolvido para modernizar o gerenciamento de encomendas em condomínios residenciais.

A proposta é facilitar o trabalho da portaria, permitir que os moradores acompanhem suas encomendas e garantir maior organização, segurança e rastreabilidade durante o processo de recebimento e retirada.

## 🚀 Funcionalidades implementadas

- Cadastro de usuários.
- Login com autenticação e senha protegida por hash.
- Controle de acesso por perfil.
- Perfil de administrador e morador.
- Cadastro e consulta de encomendas.
- Liberação de encomendas para retirada.
- Solicitação de retirada pelo morador.
- Confirmação de entrega.
- Histórico de movimentação das encomendas.
- Validação de dados.
- Controle de permissões dos usuários.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem principal.
- **SQLite:** banco de dados relacional.
- **SQL:** criação e gerenciamento das tabelas.
- **Git e GitHub:** versionamento e compartilhamento do código.
- **Flask:** tecnologia prevista para a integração da interface web.

## 🧱 Estrutura do projeto

```text
DropSmart2050/
│
├── database/
│   ├── conexao.py
│   └── schema.sql
│
├── models/
│   ├── usuario.py
│   ├── administrador.py
│   ├── morador.py
│   └── encomenda.py
│
├── services/
│   ├── usuario_service.py
│   ├── painel_service.py
│   └── encomenda_service.py
│
├── tests/
│   └── arquivos de testes
│
├── app.py
├── testar_poo.py
└── .gitignore
```

## 🔄 Fluxo das encomendas

O sistema trabalha com as seguintes etapas:

1. Recebido na portaria.
2. Disponível para retirada.
3. Solicitação de retirada.
4. Entregue.

## 👥 Perfis de acesso

**Administrador**
- Gerencia as encomendas.
- Consulta os registros.
- Libera encomendas para retirada.
- Confirma as entregas.
- Consulta o histórico.

**Morador**
- Consulta suas próprias encomendas.
- Solicita a retirada.
- Consulta o histórico de movimentações.

## 💻 Como executar o projeto

### Pré-requisitos

- Python instalado.
- Git instalado.
- Visual Studio Code (recomendado).

### 1. Clonar o repositório

```bash
git clone https://github.com/romariothedev/DropSmart2050.git
```

### 2. Entrar na pasta

```bash
cd DropSmart2050
```

### 3. Executar a aplicação

```bash
python app.py
```

O banco de dados local será preparado pela aplicação, conforme sua configuração.

## 🧪 Testes

O projeto possui arquivos de testes para verificar funcionalidades como:

- Cadastro de usuários.
- Login.
- Pilares da programação orientada a objetos.
- Cadastro de encomendas.
- Atualização de status.
- Solicitação de retirada.
- Confirmação de entrega.
- Histórico de movimentações.
- Permissões dos moradores.

## 📚 Conceitos de programação aplicados

O desenvolvimento utiliza conceitos de Programação Orientada a Objetos (POO):

- Abstração.
- Encapsulamento.
- Herança.
- Polimorfismo.

## 🔮 Próximas etapas

- Integração com Flask.
- Desenvolvimento da interface web.
- Aprimoramento da experiência do usuário.
- Evolução das funcionalidades de gestão inteligente.

## 🎓 Projeto acadêmico

**Projeto:** DropSmart 2050  
**Evento:** ExpoTech 2026.2  
**Tema:** Smart Home & Tecnologias do Futuro  
**Curso:** Análise e Desenvolvimento de Sistemas – UniFECAF

---

**DropSmart 2050 – Tecnologia, segurança e praticidade na gestão de encomendas.**


## 🌐 Interface Web (Flask)

A interface web está disponível em `web_app.py`. Consulte `README_WEB.md` para instalação, execução e funcionalidades. Instale as dependências com `pip install -r requirements.txt` e inicie com `python web_app.py`.
