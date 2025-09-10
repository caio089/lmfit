#!/usr/bin/env python
"""
Script para configurar o banco de dados no Render
Execute este script após o deploy para garantir que as tabelas sejam criadas
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

def setup_database():
    """Configura o banco de dados"""
    print("🔧 Configurando banco de dados...")
    
    try:
        # Aplicar migrações
        print("📦 Aplicando migrações...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Criar superusuário se não existir
        print("👤 Verificando superusuário...")
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@lmfit.com', 'admin123')
            print("✅ Superusuário criado: admin/admin123")
        else:
            print("ℹ️ Superusuário já existe")
            
        print("✅ Banco de dados configurado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao configurar banco de dados: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_database()
