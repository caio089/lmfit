# 🚀 Guia Completo de Deploy no Render com Supabase

## 📋 Pré-requisitos

### 1. Conta no Supabase
- ✅ Conta criada em [supabase.com](https://supabase.com)
- ✅ Projeto criado no Supabase
- ✅ Banco PostgreSQL configurado

### 2. Conta no Render
- ✅ Conta criada em [render.com](https://render.com)
- ✅ Conectado ao GitHub

### 3. Repositório GitHub
- ✅ Código enviado para o GitHub
- ✅ Repositório público ou privado (Render suporta ambos)

---

## 🔧 Passo 1: Configurar Supabase

### 1.1 Obter Credenciais do Supabase

1. **Acesse seu projeto no Supabase Dashboard**
2. **Vá em Settings → API**
3. **Copie as seguintes informações:**
   - `Project URL` (SUPABASE_URL)
   - `anon public` key (SUPABASE_KEY)
   - `service_role` key (SUPABASE_SERVICE_KEY)

### 1.2 Configurar Storage Bucket

1. **Vá em Storage no Supabase**
2. **Crie um bucket chamado `roupas`**
3. **Configure as políticas de acesso:**
   ```sql
   -- Política para leitura pública
   CREATE POLICY "Public Access" ON storage.objects
   FOR SELECT USING (bucket_id = 'roupas');
   
   -- Política para upload (apenas service_role)
   CREATE POLICY "Service Role Upload" ON storage.objects
   FOR INSERT WITH CHECK (bucket_id = 'roupas');
   ```

### 1.3 Obter Credenciais do Banco

1. **Vá em Settings → Database**
2. **Copie a Connection String**
3. **Extraia as informações:**
   - Host: `db.xxxxx.supabase.co`
   - Database: `postgres`
   - User: `postgres`
   - Password: `sua_senha`
   - Port: `5432`

---

## 🚀 Passo 2: Deploy no Render

### 2.1 Criar Web Service

1. **Acesse [Render Dashboard](https://dashboard.render.com)**
2. **Clique em "New +" → "Web Service"**
3. **Conecte ao seu repositório GitHub**
4. **Configure o serviço:**

   **Configurações Básicas:**
   - **Name**: `lmfit`
   - **Environment**: `Python 3`
   - **Region**: Escolha a mais próxima do Brasil
   - **Branch**: `main` (ou sua branch principal)
   - **Root Directory**: `LMFIT` (pasta onde está o manage.py)

   **Build & Deploy:**
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn LMFIT.wsgi:application`

### 2.2 Configurar Variáveis de Ambiente

**Adicione estas variáveis no Render:**

```bash
# Configurações básicas
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-forte-aqui

# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-anon-key-aqui
SUPABASE_SERVICE_KEY=sua-service-role-key-aqui
SUPABASE_STORAGE_BUCKET=roupas

# Banco de dados Supabase
SUPABASE_DB_HOST=db.seu-projeto.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=sua-senha-do-banco
SUPABASE_DB_PORT=5432
```

### 2.3 Gerar SECRET_KEY Segura

**Execute este comando para gerar uma chave segura:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 🗄️ Passo 3: Configurar Banco de Dados

### 3.1 Aplicar Migrações

**Após o deploy, execute no terminal do Render:**
```bash
python manage.py migrate
```

### 3.2 Criar Superusuário

**Use o comando Django:**
```bash
python manage.py setup_admin
```

**Este comando irá:**
- Criar o usuário `admin` se não existir
- Definir a senha como `luara10`
- Atualizar a senha se o usuário já existir

**Credenciais do Admin:**
- **Usuário**: `admin`
- **Senha**: `luara10`
- **Email**: `admin@lmfit.com`

---

## 🔍 Passo 4: Verificar Deploy

### 4.1 Testar URLs

- **Site principal**: `https://seu-app.onrender.com/`
- **Painel admin**: `https://seu-app.onrender.com/painel/`
- **Admin Django**: `https://seu-app.onrender.com/admin/`

### 4.2 Testar Funcionalidades

1. **Acesse o painel administrativo**
2. **Adicione uma roupa de teste**
3. **Verifique se a imagem foi enviada para o Supabase**
4. **Teste a página da loja**

---

## ⚠️ Problemas Comuns e Soluções

### Problema 1: Erro de Conexão com Banco
**Solução:**
- Verifique se as credenciais do Supabase estão corretas
- Confirme se o banco está ativo no Supabase
- Teste a conexão localmente primeiro

### Problema 2: Imagens não Carregam
**Solução:**
- Verifique se o bucket `roupas` existe no Supabase
- Confirme as políticas de acesso do Storage
- Teste o upload manualmente no Supabase

### Problema 3: Erro 500 Internal Server Error
**Solução:**
- Verifique os logs do Render
- Confirme se todas as variáveis de ambiente estão definidas
- Teste localmente com as mesmas configurações

### Problema 4: Site não Carrega
**Solução:**
- Verifique se o `ALLOWED_HOSTS` inclui `.onrender.com`
- Confirme se o `DEBUG=False` em produção
- Verifique se o `SECRET_KEY` está definido

---

## 🔄 Deploy Futuro

### Para Atualizar o Site:

1. **Faça as alterações no código**
2. **Commit e push para o GitHub:**
   ```bash
   git add .
   git commit -m "Atualização do site"
   git push origin main
   ```
3. **O Render fará o deploy automaticamente**
4. **Os dados no banco serão preservados**

---

## 📊 Monitoramento

### Logs do Render
- Acesse o dashboard do Render
- Clique no seu serviço
- Vá em "Logs" para ver erros

### Logs do Supabase
- Acesse o dashboard do Supabase
- Vá em "Logs" para ver atividade do banco

---

## 🎯 Checklist Final

- [ ] Supabase configurado com bucket `roupas`
- [ ] Variáveis de ambiente definidas no Render
- [ ] Migrações aplicadas
- [ ] Superusuário criado
- [ ] Site carregando corretamente
- [ ] Upload de imagens funcionando
- [ ] Painel administrativo acessível

---

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs do Render
2. Teste localmente com as mesmas configurações
3. Verifique se todas as variáveis estão corretas
4. Confirme se o Supabase está ativo

**URLs importantes:**
- [Render Dashboard](https://dashboard.render.com)
- [Supabase Dashboard](https://supabase.com/dashboard)
- [Documentação Render](https://render.com/docs)
- [Documentação Supabase](https://supabase.com/docs)
