#!/usr/bin/env python
"""
Script para corrigir o usuário admin
Execute no shell do Render: python fix_admin.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.production_settings')
django.setup()

from django.contrib.auth import get_user_model

def fix_admin():
    print("=== CORRIGINDO USUÁRIO ADMIN ===")
    
    try:
        User = get_user_model()
        
        # Deletar usuário admin existente
        User.objects.filter(username='admin').delete()
        print("✅ Usuário admin anterior removido")
        
        # Criar novo usuário admin
        user = User.objects.create_superuser(
            username='admin',
            email='admin@lmfit.com',
            password='luara10'
        )
        
        print("✅ Usuário admin criado com sucesso!")
        print("👤 Usuário: admin")
        print("🔑 Senha: luara10")
        
        # Verificar se foi criado
        if User.objects.filter(username='admin').exists():
            print("✅ Verificação: Usuário existe no banco")
            
            # Testar autenticação
            from django.contrib.auth import authenticate
            test_user = authenticate(username='admin', password='luara10')
            if test_user:
                print("✅ Verificação: Login funciona")
                print("🌐 Acesse: https://seu-app.onrender.com/admin/")
            else:
                print("❌ Erro: Login não funciona")
        else:
            print("❌ Erro: Usuário não foi criado")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    fix_admin()
