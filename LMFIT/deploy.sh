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
python manage.py setup_admin --settings=LMFIT.production_settings

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=LMFIT.production_settings

echo "=== DEPLOY CONCLUÍDO ==="
