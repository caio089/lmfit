# 🚀 INSTRUÇÕES DE DEPLOY - LMFIT

## 📋 Pré-requisitos

1. **Conta no Supabase** criada e configurada
2. **Conta no Render** para deploy
3. **Repositório Git** (GitHub/GitLab)

## 🔧 Configuração do Supabase

### 1. Criar Projeto no Supabase
- Acesse: https://supabase.com
- Crie um novo projeto
- Anote as credenciais

### 2. Executar Script SQL
- Vá em "SQL Editor" no Supabase
- Execute o script `script_supabase_correto.sql`
- Isso criará todas as tabelas necessárias

### 3. Configurar Storage
- Vá em "Storage" no Supabase
- Crie um bucket chamado "roupas"
- Configure as políticas de acesso

## 🌐 Deploy no Render

### 1. Conectar Repositório
- Acesse: https://render.com
- Conecte seu repositório Git
- Selecione o branch "main"

### 2. Configurar Serviço
- **Tipo**: Web Service
- **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
- **Start Command**: `gunicorn LMFIT.wsgi:application`

### 3. Variáveis de Ambiente
Configure as seguintes variáveis no Render:

```
DEBUG=False
SECRET_KEY=django-insecure-=@)s%(c6rhxjh22p1njhbcyi+r$1brb0w^ouz#!1%0*u*c-9wn
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_key_anonima
SUPABASE_SERVICE_KEY=sua_service_key
SUPABASE_STORAGE_BUCKET=roupas
SUPABASE_DB_HOST=seu_host_do_supabase
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=sua_senha_do_supabase
SUPABASE_DB_PORT=5432
```

### 4. Deploy
- Clique em "Deploy"
- Aguarde o build completar
- Acesse a URL fornecida

## ✅ Verificação Pós-Deploy

1. **Site Principal**: Acesse a URL do Render
2. **Painel Admin**: URL + `/painel/`
3. **Login**: admin / admin123
4. **Teste Upload**: Adicione uma roupa com foto

## 🔍 Troubleshooting

### Erro de Conexão com Supabase
- Verifique se as variáveis de ambiente estão corretas
- Confirme se o projeto Supabase está ativo

### Erro de Migração
- Execute: `python manage.py migrate` localmente
- Verifique se o script SQL foi executado no Supabase

### Erro de Static Files
- Execute: `python manage.py collectstatic --noinput`
- Verifique se o WhiteNoise está configurado

## 📞 Suporte

Se encontrar problemas, verifique:
1. Logs do Render
2. Status do Supabase
3. Configurações de variáveis de ambiente