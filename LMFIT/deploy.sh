#!/bin/bash

echo "=== INICIANDO DEPLOY ==="

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Executando migrações..."
python manage.py migrate --settings=LMFIT.production_settings || {
    echo "Erro na migração. Tentando --fake-initial..."
    python manage.py migrate --fake-initial --settings=LMFIT.production_settings || {
        echo "Erro com --fake-initial. Marcando migração como fake..."
        python manage.py migrate loja 0001 --fake --settings=LMFIT.production_settings
        python manage.py migrate --settings=LMFIT.production_settings
    }
}

echo "Criando usuário admin..."
python manage.py shell --settings=LMFIT.production_settings << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(username='admin').delete()
User.objects.create_superuser('admin', 'admin@lmfit.com', 'luara10')
print("Usuário admin criado: admin / luara10")
EOF

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=LMFIT.production_settings

echo "=== DEPLOY CONCLUÍDO ==="
