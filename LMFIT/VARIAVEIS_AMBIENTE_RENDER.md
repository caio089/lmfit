# 🔧 Variáveis de Ambiente para o Render

## ⚠️ IMPORTANTE: Configure estas variáveis no Render Dashboard

### 1. Acesse o Render Dashboard
- Vá em [render.com](https://render.com)
- Clique no seu serviço `lmfit`
- Vá em "Environment"

### 2. Adicione estas variáveis:

```bash
# Configurações básicas
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-forte-aqui

# Supabase - SUBSTITUA pelos seus valores reais
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

### 3. Como obter os valores do Supabase:

#### SUPABASE_URL e SUPABASE_KEY:
1. Acesse [supabase.com](https://supabase.com)
2. Vá em Settings → API
3. Copie:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** key → `SUPABASE_KEY`
   - **service_role** key → `SUPABASE_SERVICE_KEY`

#### Credenciais do Banco:
1. Vá em Settings → Database
2. Copie a **Connection string**
3. Extraia as informações:
   - **Host**: `db.xxxxx.supabase.co` → `SUPABASE_DB_HOST`
   - **Password**: sua senha → `SUPABASE_DB_PASSWORD`

### 4. Gerar SECRET_KEY:
Execute este comando Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 5. Após configurar:
1. Salve as variáveis no Render
2. Faça um novo deploy
3. Teste o site

## 🚨 Problemas Comuns:

### Erro 500 - Verificar:
1. ✅ Todas as variáveis estão definidas?
2. ✅ Credenciais do Supabase estão corretas?
3. ✅ Banco de dados está ativo no Supabase?
4. ✅ Bucket `roupas` existe no Supabase Storage?

### Logs do Render:
- Acesse o dashboard do Render
- Clique em "Logs" para ver erros detalhados
