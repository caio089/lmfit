#!/usr/bin/env python
"""
Script para testar upload através da view Django
"""
import os
import sys
import django
from pathlib import Path
from django.test import RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import AnonymousUser

# Adicionar o diretório do projeto ao path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.views import admin_roupa_add
from PIL import Image
import io

def test_view_upload():
    """Testa o upload através da view"""
    print("🧪 TESTANDO UPLOAD ATRAVÉS DA VIEW")
    print("=" * 50)
    
    # Criar uma imagem de teste
    print("📸 Criando imagem de teste...")
    img = Image.new('RGB', (200, 200), color='blue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    # Criar arquivo de upload
    test_file = SimpleUploadedFile(
        "test_view.jpg",
        img_byte_arr.getvalue(),
        content_type="image/jpeg"
    )
    
    # Simular request POST
    factory = RequestFactory()
    request = factory.post('/painel/roupas/add/', {
        'nome': 'Teste View Upload',
        'descricao': 'Teste de upload através da view',
        'preco': '99.90',
        'categoria': 'tops',
        'tamanhos_disponiveis': 'P,M,G',
        'ativo': 'on'
    })
    request.FILES['foto_principal'] = test_file
    request.user = AnonymousUser()
    
    print("🚀 Testando upload através da view...")
    
    try:
        # Importar a função de upload diretamente
        from loja.supabase_direct import upload_image_to_supabase
        
        result = upload_image_to_supabase(test_file, "roupas")
        
        if result['success']:
            print("✅ Upload através da view funcionou!")
            print(f"   URL: {result['public_url']}")
            print(f"   Path: {result['storage_path']}")
            return True
        else:
            print(f"❌ Erro no upload: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na view: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_view_upload()
    if success:
        print("\n🎉 Teste da view passou!")
    else:
        print("\n💥 Teste da view falhou!")
        sys.exit(1)
