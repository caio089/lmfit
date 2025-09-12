#!/usr/bin/env python
"""
Script para verificar configurações antes do deploy
Execute: python check_config.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

def check_config():
    print("🔍 Verificando configurações do projeto...")
    
    # Verificar variáveis de ambiente
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_KEY', 
        'SUPABASE_SERVICE_KEY',
        'SUPABASE_DB_HOST',
        'SUPABASE_DB_PASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Variáveis de ambiente faltando:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Configure essas variáveis no Render Dashboard")
        return False
    
    print("✅ Todas as variáveis de ambiente estão configuradas")
    
    # Verificar configurações do Django
    from django.conf import settings
    
    print(f"✅ DEBUG: {settings.DEBUG}")
    print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"✅ SECRET_KEY: {'Configurada' if settings.SECRET_KEY else 'Não configurada'}")
    
    # Verificar banco de dados
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Conexão com banco de dados: OK")
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False
    
    # Verificar Supabase
    try:
        from loja.supabase_utils import get_supabase_client
        client = get_supabase_client()
        if client:
            print("✅ Conexão com Supabase: OK")
        else:
            print("❌ Erro na conexão com Supabase")
            return False
    except Exception as e:
        print(f"❌ Erro na conexão com Supabase: {e}")
        return False
    
    print("\n🎉 Todas as configurações estão corretas!")
    print("🚀 Pronto para deploy no Render!")
    
    return True

if __name__ == '__main__':
    check_config()
