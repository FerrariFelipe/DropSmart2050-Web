# Publicar DropSmart 2050 gratuitamente no Render (demo)

## Antes de publicar

1. Envie este projeto para um repositório GitHub.
2. No Render, crie um **New + Web Service** e conecte o repositório.
3. Use estas configurações:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT web_app:app`
   - Instance Type: Free
4. Em **Environment**, crie estas variáveis:
   - `DROPSMART_SECRET`: uma chave longa, aleatória e exclusiva.
   - `DROPSMART_ADMIN_NOME`: nome do administrador inicial.
   - `DROPSMART_ADMIN_EMAIL`: e-mail do administrador inicial.
   - `DROPSMART_ADMIN_SENHA`: senha forte do administrador inicial.
5. Salve e aguarde o deploy. O Render fornecerá um endereço `*.onrender.com`.

O administrador inicial é criado automaticamente na inicialização se o e-mail ainda não existir no banco. Não compartilhe as variáveis de ambiente nem coloque senhas no GitHub.

## Limitação importante do plano gratuito

O serviço gratuito do Render pode dormir após 15 minutos sem acessos e demora aproximadamente um minuto para voltar. O sistema atual usa SQLite em arquivo local; no Render Free, esse arquivo é efêmero e pode ser apagado em reinicializações, suspensão ou novo deploy. Portanto, use esta publicação somente para demonstração com dados fictícios e esteja preparado para recriar os cadastros. Não use dados pessoais/reais de moradores nem para operação real de condomínio. Para dados persistentes, será necessário migrar para banco externo persistente; o Postgres gratuito do Render também tem prazo de expiração de 30 dias.
