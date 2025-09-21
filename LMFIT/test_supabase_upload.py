#!/usr/bin/env python
"""
Script para testar upload no Supabase Storage
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

from loja.supabase_direct import test_supabase_connection, upload_image_to_supabase
from django.core.files.uploadedfile import SimpleUploadedFile
import io

def test_upload():
    """Testa o upload de uma imagem"""
    print("🧪 TESTANDO UPLOAD NO SUPABASE")
    print("=" * 50)
    
    # Testar conexão primeiro
    if not test_supabase_connection():
        print("❌ Falha na conexão com Supabase")
        return False
    
    # Criar uma imagem de teste
    print("\n📸 Criando imagem de teste...")
    
    # Criar uma imagem simples em memória
    from PIL import Image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    # Criar arquivo de upload simulado
    test_file = SimpleUploadedFile(
        "test_image.jpg",
        img_byte_arr.getvalue(),
        content_type="image/jpeg"
    )
    
    print("🚀 Fazendo upload de teste...")
    
    # Fazer upload
    result = upload_image_to_supabase(test_file, "test")
    
    if result['success']:
        print("✅ Upload realizado com sucesso!")
        print(f"   URL: {result['public_url']}")
        print(f"   Path: {result['storage_path']}")
        return True
    else:
        print(f"❌ Erro no upload: {result['error']}")
        return False

if __name__ == "__main__":
    success = test_upload()
    if success:
        print("\n🎉 Teste de upload passou!")
    else:
        print("\n💥 Teste de upload falhou!")
        sys.exit(1)
