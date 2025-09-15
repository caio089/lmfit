#!/usr/bin/env python
"""
Teste simples do Supabase
Execute: python test_supabase_simple.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.production_settings')
django.setup()

def test_supabase():
    print("=== TESTE SIMPLES DO SUPABASE ===")
    
    try:
        from supabase import create_client
        
        # Valores fixos
        SUPABASE_URL = "https://ubasgcbrwjdbhtxandrm.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViYXNnY2Jyd2pkYmh0eGFuZHJtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc3NjY2OTAsImV4cCI6MjA3MzM0MjY5MH0.jOWVQq_Yrl0LkFLj2IK2B0l1aHv2Pl5dxgne944eq5o"
        
        print(f"URL: {SUPABASE_URL}")
        print(f"KEY: {SUPABASE_KEY[:50]}...")
        
        # Criar cliente
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Cliente criado com sucesso!")
        
        # Testar conexão
        try:
            buckets = client.storage.list_buckets()
            print("✅ Conexão funcionando!")
            print(f"Buckets encontrados: {len(buckets)}")
            
            # Verificar se bucket 'roupas' existe
            bucket_names = [bucket['name'] for bucket in buckets]
            if 'roupas' in bucket_names:
                print("✅ Bucket 'roupas' encontrado!")
            else:
                print("❌ Bucket 'roupas' não encontrado")
                print(f"Buckets disponíveis: {bucket_names}")
                
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            
    except ImportError as e:
        print(f"❌ Supabase não instalado: {e}")
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_supabase()
