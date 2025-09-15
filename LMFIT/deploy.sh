#!/bin/bash

echo "=== INICIANDO DEPLOY ==="

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Verificando estado do banco..."
python manage.py check_db --settings=LMFIT.production_settings

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=LMFIT.production_settings

echo "=== DEPLOY CONCLUÍDO ==="
