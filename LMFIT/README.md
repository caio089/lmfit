# LMFIT - Loja de Roupas Fitness Femininas

Sistema de e-commerce para roupas fitness femininas com painel administrativo integrado ao Supabase.

## 🚀 Funcionalidades

- **Loja Online**: Exibição de produtos com fotos e informações
- **Painel Admin**: Gerenciamento de produtos e upload de imagens
- **Supabase Integration**: Banco PostgreSQL + Storage para imagens
- **Design Responsivo**: Interface moderna e mobile-friendly

## 🛠️ Tecnologias

- **Backend**: Django 5.2.5
- **Database**: Supabase PostgreSQL
- **Storage**: Supabase Storage
- **Frontend**: HTML5, CSS3, Tailwind CSS, JavaScript
- **Deploy**: Render

## 📋 Configuração para Deploy

### Variáveis de Ambiente Necessárias:

```env
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

### Comandos de Deploy:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn LMFIT.wsgi:application
```

## 🗄️ Estrutura do Banco

O projeto usa as seguintes tabelas principais:
- `loja_roupa`: Produtos da loja
- `auth_user`: Usuários do sistema
- Tabelas padrão do Django

## 📱 Acesso

- **Site**: URL do Render
- **Admin**: `/painel/`
- **Login**: admin / admin123

## 🔧 Desenvolvimento Local

```bash
cd LMFIT
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/
