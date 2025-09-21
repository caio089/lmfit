#!/usr/bin/env python
"""
Script para debugar o upload exatamente como na view
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

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

def debug_upload():
    """Debuga o upload exatamente como na view"""
    print("🐛 DEBUGANDO UPLOAD COMO NA VIEW")
    print("=" * 50)
    
    # Criar imagem de teste
    print("📸 Criando imagem de teste...")
    img = Image.new('RGB', (300, 300), color='purple')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=85)
    img_byte_arr.seek(0)
    
    # Simular exatamente como o Django recebe o arquivo
    test_file = SimpleUploadedFile(
        "debug_test.jpg",
        img_byte_arr.getvalue(),
        content_type="image/jpeg"
    )
    
    print(f"📁 Arquivo criado:")
    print(f"   Nome: {test_file.name}")
    print(f"   Tamanho: {test_file.size} bytes")
    print(f"   Content-Type: {test_file.content_type}")
    
    # Testar upload exatamente como na view
    print("\n🚀 Testando upload como na view...")
    
    try:
        from loja.supabase_direct import upload_image_to_supabase
        
        # Simular exatamente o que acontece na view
        upload_result = upload_image_to_supabase(
            test_file, 
            folder_name="roupas"
        )
        
        print(f"📊 Resultado do upload:")
        print(f"   Success: {upload_result['success']}")
        print(f"   Error: {upload_result.get('error', 'Nenhum')}")
        print(f"   Public URL: {upload_result.get('public_url', 'Nenhuma')}")
        print(f"   Storage Path: {upload_result.get('storage_path', 'Nenhum')}")
        
        if upload_result['success']:
            print("\n✅ Upload funcionou perfeitamente!")
            return True
        else:
            print(f"\n❌ Erro no upload: {upload_result['error']}")
            return False
            
    except Exception as e:
        print(f"\n❌ Erro na execução: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_upload()
    if success:
        print("\n🎉 Debug passou!")
    else:
        print("\n💥 Debug falhou!")
        sys.exit(1)
