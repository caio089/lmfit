#!/usr/bin/env python
"""
Script para migrar imagens existentes do BinaryField para Cloudinary
Execute este script apenas se você já tem produtos cadastrados com imagens em BinaryField
"""

import os
import sys
import django
from io import BytesIO

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.models import Roupa
from cloudinary import uploader
import base64

def migrate_images_to_cloudinary():
    """
    Migra imagens existentes do BinaryField para Cloudinary
    """
    print("Iniciando migração de imagens para Cloudinary...")
    
    roupas = Roupa.objects.all()
    total_roupas = roupas.count()
    print(f"Encontradas {total_roupas} roupas para migrar")
    
    if total_roupas == 0:
        print("Nenhuma roupa encontrada. Migração não necessária.")
        return
    
    migrated_count = 0
    
    for roupa in roupas:
        print(f"\nProcessando: {roupa.nome}")
        
        # Verificar se já tem URLs do Cloudinary
        if hasattr(roupa, 'foto_principal') and roupa.foto_principal and hasattr(roupa.foto_principal, 'url'):
            print("  - Já migrado para Cloudinary")
            continue
        
        try:
            # Migrar foto principal se existir
            if hasattr(roupa, 'foto_principal') and roupa.foto_principal:
                if isinstance(roupa.foto_principal, bytes):
                    print("  - Migrando foto principal...")
                    
                    # Converter bytes para arquivo temporário
                    image_data = BytesIO(roupa.foto_principal)
                    
                    # Upload para Cloudinary
                    result = uploader.upload(
                        image_data,
                        public_id=f"roupas/{roupa.id}/foto_principal",
                        folder="lmfit/produtos"
                    )
                    
                    # Atualizar o campo
                    roupa.foto_principal = result['public_id']
                    print(f"    ✅ Foto principal migrada: {result['url']}")
                
            # Migrar foto 2 se existir
            if hasattr(roupa, 'foto_2') and roupa.foto_2:
                if isinstance(roupa.foto_2, bytes):
                    print("  - Migrando foto 2...")
                    
                    image_data = BytesIO(roupa.foto_2)
                    result = uploader.upload(
                        image_data,
                        public_id=f"roupas/{roupa.id}/foto_2",
                        folder="lmfit/produtos"
                    )
                    
                    roupa.foto_2 = result['public_id']
                    print(f"    ✅ Foto 2 migrada: {result['url']}")
                
            # Migrar foto 3 se existir
            if hasattr(roupa, 'foto_3') and roupa.foto_3:
                if isinstance(roupa.foto_3, bytes):
                    print("  - Migrando foto 3...")
                    
                    image_data = BytesIO(roupa.foto_3)
                    result = uploader.upload(
                        image_data,
                        public_id=f"roupas/{roupa.id}/foto_3",
                        folder="lmfit/produtos"
                    )
                    
                    roupa.foto_3 = result['public_id']
                    print(f"    ✅ Foto 3 migrada: {result['url']}")
            
            # Salvar as alterações
            roupa.save()
            migrated_count += 1
            print(f"  ✅ {roupa.nome} migrada com sucesso!")
            
        except Exception as e:
            print(f"  ❌ Erro ao migrar {roupa.nome}: {str(e)}")
            continue
    
    print(f"\n🎉 Migração concluída!")
    print(f"✅ {migrated_count} roupas migradas com sucesso")
    print(f"📁 Imagens salvas no Cloudinary em: lmfit/produtos/")

if __name__ == "__main__":
    print("=== MIGRAÇÃO PARA CLOUDINARY ===")
    print("Este script migrará imagens existentes para o Cloudinary")
    print("Certifique-se de que as configurações do Cloudinary estão corretas")
    
    resposta = input("\nDeseja continuar? (s/N): ").lower()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        migrate_images_to_cloudinary()
    else:
        print("Migração cancelada.")
