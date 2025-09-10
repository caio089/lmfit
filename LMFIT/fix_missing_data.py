#!/usr/bin/env python
"""
Script para corrigir dados perdidos no Render
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.models import Roupa
from django.contrib.auth.models import User

def check_and_fix_data():
    """Verifica e corrige dados perdidos"""
    print("🔍 Verificando dados no banco...")
    
    # Verificar roupas
    roupas_count = Roupa.objects.count()
    print(f"👕 Total de roupas: {roupas_count}")
    
    if roupas_count == 0:
        print("⚠️ Nenhuma roupa encontrada! Criando dados de exemplo...")
        
        # Criar algumas roupas de exemplo
        roupas_exemplo = [
            {
                'nome': 'Top Básico Rosa',
                'descricao': 'Top confortável para treinos, feito com tecido respirável e tecnologia anti-odor.',
                'preco': 89.90,
                'categoria': 'tops',
                'tamanhos_disponiveis': 'P,M,G',
                'ativo': True
            },
            {
                'nome': 'Legging Preta Premium',
                'descricao': 'Legging de alta qualidade com cintura alta e tecnologia de compressão.',
                'preco': 149.90,
                'categoria': 'leggings',
                'tamanhos_disponiveis': 'P,M,G,GG',
                'ativo': True
            },
            {
                'nome': 'Conjunto Completo',
                'descricao': 'Conjunto coordenado com top e legging, perfeito para treinos intensos.',
                'preco': 199.90,
                'categoria': 'conjuntos',
                'tamanhos_disponiveis': 'P,M,G',
                'ativo': True
            },
            {
                'nome': 'Blusa Oversized',
                'descricao': 'Blusa confortável e estilosa, ideal para o dia a dia.',
                'preco': 79.90,
                'categoria': 'blusas',
                'tamanhos_disponiveis': 'P,M,G',
                'ativo': True
            },
            {
                'nome': 'Acessório Fitness',
                'descricao': 'Acessório essencial para completar seu look fitness.',
                'preco': 39.90,
                'categoria': 'acessorios',
                'tamanhos_disponiveis': 'Único',
                'ativo': True
            }
        ]
        
        for roupa_data in roupas_exemplo:
            # Criar roupa sem fotos por enquanto
            roupa = Roupa.objects.create(
                nome=roupa_data['nome'],
                descricao=roupa_data['descricao'],
                preco=roupa_data['preco'],
                categoria=roupa_data['categoria'],
                tamanhos_disponiveis=roupa_data['tamanhos_disponiveis'],
                ativo=roupa_data['ativo'],
                foto_principal=b'',  # Foto vazia por enquanto
                foto_2=b'',
                foto_3=b''
            )
            print(f"✅ Criada: {roupa.nome}")
        
        print(f"✅ {len(roupas_exemplo)} roupas de exemplo criadas!")
    else:
        print("✅ Roupas encontradas no banco!")
    
    # Verificar usuário admin
    if not User.objects.filter(username='admin').exists():
        print("👤 Criando usuário admin...")
        User.objects.create_superuser(
            username='admin',
            email='luaracarvalho10@icloud.com',
            password='luara10'
        )
        print("✅ Usuário admin criado!")
    else:
        print("✅ Usuário admin já existe!")
    
    print("\n🎉 Verificação e correção concluídas!")

if __name__ == "__main__":
    check_and_fix_data()
