#!/usr/bin/env python
"""
Script para verificar e corrigir problemas de banco de dados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.models import Roupa
from django.db import connection
from django.conf import settings

def check_database():
    """Verifica a configuração do banco de dados"""
    print("🔍 Verificando configuração do banco de dados...")
    
    # Verificar configuração
    db_config = settings.DATABASES['default']
    print(f"📊 Engine: {db_config['ENGINE']}")
    print(f"📊 Name: {db_config.get('NAME', 'N/A')}")
    print(f"📊 Host: {db_config.get('HOST', 'N/A')}")
    print(f"📊 Port: {db_config.get('PORT', 'N/A')}")
    
    # Verificar conexão
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Conexão com banco OK")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    
    # Verificar tabelas
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📋 Tabelas encontradas: {[t[0] for t in tables]}")
    except Exception as e:
        print(f"❌ Erro ao listar tabelas: {e}")
    
    # Verificar roupas
    try:
        count = Roupa.objects.count()
        print(f"👕 Total de roupas: {count}")
        
        if count > 0:
            print("📝 Roupas encontradas:")
            for roupa in Roupa.objects.all()[:5]:  # Mostrar apenas as primeiras 5
                print(f"  - {roupa.nome} ({roupa.categoria}) - R$ {roupa.preco}")
        else:
            print("⚠️ Nenhuma roupa encontrada no banco!")
            
    except Exception as e:
        print(f"❌ Erro ao consultar roupas: {e}")
        return False
    
    return True

def check_environment():
    """Verifica variáveis de ambiente"""
    print("\n🌍 Verificando variáveis de ambiente...")
    print(f"RENDER: {os.getenv('RENDER', 'Não definido')}")
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'Não definido')}")
    print(f"DEBUG: {os.getenv('DEBUG', 'Não definido')}")

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DO BANCO DE DADOS")
    print("=" * 50)
    
    check_environment()
    success = check_database()
    
    if success:
        print("\n✅ Diagnóstico concluído com sucesso!")
    else:
        print("\n❌ Problemas encontrados no banco de dados!")
        sys.exit(1)
