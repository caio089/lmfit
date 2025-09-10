#!/usr/bin/env python
"""
Script para corrigir o problema de perda de dados no Render
Execute: python fix_database.py
"""

import os
import django
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

def fix_database():
    """Corrige a configuração do banco de dados"""
    print("🔧 CORRIGINDO CONFIGURAÇÃO DO BANCO DE DADOS")
    print("=" * 50)
    
    try:
        # Aplicar migrações
        print("📦 Aplicando migrações...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Criar superusuário
        print("👤 Criando superusuário...")
        from django.contrib.auth.models import User
        
        # Remover admin antigo se existir
        if User.objects.filter(username='admin').exists():
            User.objects.filter(username='admin').delete()
            print("✅ Usuário admin antigo removido")
        
        # Criar novo admin
        user = User.objects.create_superuser(
            username='admin',
            email='luaracarvalho10@icloud.com',
            password='luara10'
        )
        
        print("✅ Superusuário criado:")
        print("👤 Usuário: admin")
        print("📧 Email: luaracarvalho10@icloud.com")
        print("🔑 Senha: luara10")
        
        print("\n🚀 CONFIGURAÇÃO CONCLUÍDA!")
        print("Agora faça o deploy seguindo as instruções em DEPLOY_INSTRUCTIONS.md")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    fix_database()
