#!/usr/bin/env python
"""
Script para migrar dados no Render após deploy
Este script deve ser executado após cada deploy para garantir que os dados sejam migrados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.models import Roupa
from django.contrib.auth.models import User

def migrate_categories():
    """Migra categorias de 'calcinha-sem-costura' para 'acessorios'"""
    try:
        # Buscar todas as roupas com categoria 'calcinha-sem-costura'
        roupas_para_migrar = Roupa.objects.filter(categoria='calcinha-sem-costura')
        
        print(f"Encontradas {roupas_para_migrar.count()} roupas para migrar...")
        
        # Migrar cada roupa
        for roupa in roupas_para_migrar:
            print(f"Migrando: {roupa.nome} (ID: {roupa.id})")
            roupa.categoria = 'acessorios'
            roupa.save()
        
        print(f"✅ Migração de categorias concluída! {roupas_para_migrar.count()} roupas migradas")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante migração de categorias: {e}")
        return False

def create_admin_user():
    """Cria usuário admin se não existir"""
    try:
        # Verificar se já existe um superusuário
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Usuário admin já existe")
            return True
        
        # Criar superusuário
        User.objects.create_superuser(
            username='admin',
            email='luaracarvalho10@icloud.com',
            password='luara10'
        )
        print("✅ Usuário admin criado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        return False

def main():
    """Função principal"""
    print("🔄 Iniciando migração de dados no Render...")
    
    # Migrar categorias
    categories_success = migrate_categories()
    
    # Criar usuário admin
    admin_success = create_admin_user()
    
    if categories_success and admin_success:
        print("✅ Todas as migrações foram concluídas com sucesso!")
        print("📊 Dados preservados e atualizados no Render")
        return True
    else:
        print("❌ Algumas migrações falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
