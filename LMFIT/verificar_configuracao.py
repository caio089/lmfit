#!/usr/bin/env python
"""
Script para verificar se todas as configurações estão corretas
Execute este script antes do deploy para garantir que tudo está funcionando
"""

import os
import sys
import django
from pathlib import Path

# Adicionar o diretório do projeto ao path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from django.conf import settings
from django.db import connection
import requests

def verificar_variaveis_ambiente():
    """Verifica se todas as variáveis de ambiente estão definidas"""
    print("🔍 VERIFICANDO VARIÁVEIS DE AMBIENTE")
    print("=" * 50)
    
    variaveis_obrigatorias = [
        'SECRET_KEY',
        'SUPABASE_URL',
        'SUPABASE_KEY', 
        'SUPABASE_SERVICE_KEY',
        'DATABASE_URL'
    ]
    
    todas_ok = True
    
    for var in variaveis_obrigatorias:
        valor = os.getenv(var)
        if valor:
            if var == 'SECRET_KEY':
                print(f"✅ {var}: {'*' * 20}...{valor[-4:]}")
            elif 'KEY' in var or 'URL' in var:
                print(f"✅ {var}: {valor[:30]}...")
            else:
                print(f"✅ {var}: {valor}")
        else:
            print(f"❌ {var}: NÃO DEFINIDA")
            todas_ok = False
    
    print(f"\n{'✅ TODAS AS VARIÁVEIS OK' if todas_ok else '❌ FALTAM VARIÁVEIS'}")
    return todas_ok

def verificar_conexao_banco():
    """Verifica se a conexão com o banco está funcionando"""
    print("\n🔍 VERIFICANDO CONEXÃO COM BANCO")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            resultado = cursor.fetchone()
            if resultado:
                print("✅ Conexão com banco: OK")
                
                # Verificar se as tabelas existem
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name IN ('loja_roupa', 'loja_adminuser')
                    ORDER BY table_name
                """)
                tabelas = cursor.fetchall()
                
                tabelas_encontradas = [t[0] for t in tabelas]
                print(f"✅ Tabelas encontradas: {', '.join(tabelas_encontradas)}")
                
                if len(tabelas_encontradas) == 2:
                    print("✅ Estrutura do banco: OK")
                    return True
                else:
                    print("❌ Faltam tabelas no banco")
                    return False
            else:
                print("❌ Conexão com banco: FALHOU")
                return False
                
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def verificar_supabase_storage():
    """Verifica se o Supabase Storage está acessível"""
    print("\n🔍 VERIFICANDO SUPABASE STORAGE")
    print("=" * 50)
    
    try:
        url = f"{settings.SUPABASE_URL}/storage/v1/bucket"
        headers = {
            'Authorization': f'Bearer {settings.SUPABASE_KEY}'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            buckets = response.json()
            bucket_names = [bucket.get('name', '') for bucket in buckets]
            
            print(f"✅ Conexão com Supabase: OK")
            print(f"✅ Buckets disponíveis: {', '.join(bucket_names)}")
            
            if settings.SUPABASE_STORAGE_BUCKET in bucket_names:
                print(f"✅ Bucket '{settings.SUPABASE_STORAGE_BUCKET}': ENCONTRADO")
                return True
            else:
                print(f"❌ Bucket '{settings.SUPABASE_STORAGE_BUCKET}': NÃO ENCONTRADO")
                return False
        else:
            print(f"❌ Erro na API do Supabase: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

def verificar_configuracoes_django():
    """Verifica configurações do Django"""
    print("\n🔍 VERIFICANDO CONFIGURAÇÕES DJANGO")
    print("=" * 50)
    
    # Verificar DEBUG
    if settings.DEBUG:
        print("⚠️  DEBUG: True (OK para desenvolvimento)")
    else:
        print("✅ DEBUG: False (OK para produção)")
    
    # Verificar ALLOWED_HOSTS
    hosts = settings.ALLOWED_HOSTS
    print(f"✅ ALLOWED_HOSTS: {hosts}")
    
    # Verificar STATIC_ROOT
    static_root = settings.STATIC_ROOT
    if static_root and Path(static_root).exists():
        print(f"✅ STATIC_ROOT: {static_root} (existe)")
    else:
        print(f"⚠️  STATIC_ROOT: {static_root} (não existe ainda)")
    
    return True

def main():
    """Função principal"""
    print("🚀 VERIFICAÇÃO DE CONFIGURAÇÃO - LMFIT")
    print("=" * 60)
    
    resultados = []
    
    # Executar todas as verificações
    resultados.append(verificar_variaveis_ambiente())
    resultados.append(verificar_conexao_banco())
    resultados.append(verificar_supabase_storage())
    resultados.append(verificar_configuracoes_django())
    
    # Resultado final
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)
    
    if all(resultados):
        print("🎉 TODAS AS VERIFICAÇÕES PASSARAM!")
        print("✅ Seu projeto está pronto para o deploy!")
        return 0
    else:
        print("❌ ALGUMAS VERIFICAÇÕES FALHARAM!")
        print("⚠️  Corrija os problemas antes do deploy.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
