#!/usr/bin/env bash
# Script de build para o Render

echo "🚀 Iniciando build do LMFIT..."

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Aplicar migrações
echo "🗄️ Aplicando migrações do banco de dados..."
python manage.py migrate

# Executar migração de dados
echo "🔄 Executando migração de dados..."
python migrate_data.py

# Criar superusuário se não existir
echo "👤 Configurando superusuário..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'luaracarvalho10@icloud.com', 'luara10')
    print('✅ Superusuário criado: admin/luara10')
else:
    print('ℹ️ Superusuário já existe')
"

echo "✅ Build concluído com sucesso!"
