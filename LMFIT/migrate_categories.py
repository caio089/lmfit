#!/usr/bin/env python
"""
Script para migrar categorias de 'calcinha-sem-costura' para 'acessorios'
Execute este script antes de fazer deploy para garantir que os dados sejam migrados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.models import Roupa

def migrate_categories():
    """Migra todas as roupas de 'calcinha-sem-costura' para 'acessorios'"""
    try:
        # Buscar todas as roupas com categoria 'calcinha-sem-costura'
        roupas_para_migrar = Roupa.objects.filter(categoria='calcinha-sem-costura')
        
        print(f"Encontradas {roupas_para_migrar.count()} roupas para migrar...")
        
        # Migrar cada roupa
        for roupa in roupas_para_migrar:
            print(f"Migrando: {roupa.nome} (ID: {roupa.id})")
            roupa.categoria = 'acessorios'
            roupa.save()
        
        print(f"✅ Migração concluída! {roupas_para_migrar.count()} roupas migradas para 'acessorios'")
        
        # Verificar se ainda existem roupas com a categoria antiga
        roupas_antigas = Roupa.objects.filter(categoria='calcinha-sem-costura')
        if roupas_antigas.exists():
            print(f"⚠️  Ainda existem {roupas_antigas.count()} roupas com categoria antiga!")
        else:
            print("✅ Todas as roupas foram migradas com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔄 Iniciando migração de categorias...")
    success = migrate_categories()
    
    if success:
        print("✅ Migração concluída com sucesso!")
        print("📝 Agora você pode fazer o deploy no Render com segurança.")
    else:
        print("❌ Falha na migração. Verifique os erros acima.")
        sys.exit(1)
