#!/usr/bin/env python
"""
Script para criar usuário admin manualmente
Execute: python create_admin_manual.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.production_settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction

def create_admin():
    print("=== CRIANDO USUÁRIO ADMIN ===")
    
    try:
        User = get_user_model()
        
        with transaction.atomic():
            # Deletar usuário admin existente
            User.objects.filter(username='admin').delete()
            print("✅ Usuário admin anterior removido")
            
            # Criar novo usuário
            user = User.objects.create_superuser(
                username='admin',
                email='admin@lmfit.com',
                password='luara10',
                first_name='Admin',
                last_name='LMFIT'
            )
            
            print("✅ Usuário admin criado com sucesso!")
            print(f"👤 Usuário: admin")
            print(f"🔑 Senha: luara10")
            print(f"📧 Email: admin@lmfit.com")
            
            # Verificar criação
            if User.objects.filter(username='admin').exists():
                print("✅ Verificação: Usuário existe no banco")
                
                # Testar autenticação
                from django.contrib.auth import authenticate
                test_user = authenticate(username='admin', password='luara10')
                if test_user:
                    print("✅ Verificação: Login funciona")
                    print("🌐 Acesse: https://seu-app.onrender.com/painel/")
                else:
                    print("❌ Erro: Login não funciona")
            else:
                print("❌ Erro: Usuário não foi criado")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    create_admin()
