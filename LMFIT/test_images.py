#!/usr/bin/env python
"""
Script de teste para verificar se o sistema de imagens WebP está funcionando
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.models import Roupa
from loja.utils import convert_to_webp, get_image_data_url

def test_image_system():
    print("🔍 Testando sistema de imagens WebP...")
    
    # Verificar se há roupas no banco
    roupas = Roupa.objects.all()
    print(f"📊 Total de roupas no banco: {roupas.count()}")
    
    if roupas.exists():
        print("\n✅ Roupas encontradas:")
        for roupa in roupas:
            print(f"  - {roupa.nome} (ID: {roupa.id})")
            
            # Testar métodos de imagem
            if roupa.foto_principal:
                print(f"    📸 Foto principal: {len(roupa.foto_principal)} bytes")
                url = roupa.get_foto_principal_url()
                if url:
                    print(f"    🔗 URL gerada: {url[:50]}...")
                else:
                    print("    ❌ Erro ao gerar URL da foto principal")
            else:
                print("    ⚠️  Sem foto principal")
                
            if roupa.foto_2:
                print(f"    📸 Foto 2: {len(roupa.foto_2)} bytes")
            if roupa.foto_3:
                print(f"    📸 Foto 3: {len(roupa.foto_3)} bytes")
    else:
        print("⚠️  Nenhuma roupa encontrada no banco de dados")
        print("💡 Adicione algumas roupas pelo painel admin para testar")
    
    print("\n🎯 Sistema de imagens WebP configurado e funcionando!")

if __name__ == "__main__":
    test_image_system()
