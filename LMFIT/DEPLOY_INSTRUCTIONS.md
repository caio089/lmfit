# 🚀 Instruções de Deploy no Render

## 📋 Configuração do Banco de Dados

### ⚠️ PROBLEMA: Dados são perdidos a cada deploy
**SOLUÇÃO:** Configure um banco PostgreSQL persistente

### 1. Criar Banco PostgreSQL no Render
1. Acesse o [Render Dashboard](https://dashboard.render.com)
2. Clique em "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `lmfit-db`
   - **Database**: `lmfit`
   - **User**: `lmfit_user`
   - **Region**: Escolha a mais próxima
   - **Plan**: Free (ou pago se preferir)
4. **AGUARDE** o banco ser criado completamente

### 2. Configurar Web Service
1. Clique em "New +" → "Web Service"
2. Conecte ao seu repositório GitHub
3. Configure:
   - **Name**: `lmfit-web`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn LMFIT.LMFIT.wsgi`

### 3. Variáveis de Ambiente
Adicione estas variáveis no Web Service:
- `DATABASE_URL`: (será preenchida automaticamente pelo banco PostgreSQL)
- `SECRET_KEY`: (gere uma chave secreta forte)
- `DEBUG`: `False`
- `RENDER`: `True`

### 4. Ordem de Criação
**IMPORTANTE**: Crie primeiro o banco PostgreSQL, depois o Web Service:
1. Primeiro: Crie o banco PostgreSQL
2. Depois: Crie o Web Service e conecte ao banco

## 🔧 Configuração Automática

O projeto já está configurado para:
- ✅ Usar PostgreSQL no Render
- ✅ Aplicar migrações automaticamente
- ✅ Coletar arquivos estáticos
- ✅ Criar superusuário automaticamente

## 📱 Acesso ao Admin

Após o deploy:
- **URL**: `https://seu-app.onrender.com/admin/`
- **Usuário**: `admin`
- **Senha**: `admin123`

## 🎯 Resultado

Após seguir estas instruções:
- ✅ As roupas adicionadas no painel **NÃO** serão perdidas
- ✅ O banco de dados será **persistente**
- ✅ Cada deploy manterá os dados existentes
- ✅ Apenas o código será atualizado

## 🔄 Deploy Futuro

Para futuros deploys:
1. Faça push para o GitHub
2. O Render fará o deploy automaticamente
3. As roupas continuarão no banco de dados
4. Apenas o código será atualizado
