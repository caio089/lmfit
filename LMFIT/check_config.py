#!/usr/bin/env python
"""
Script para verificar configurações do Supabase
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

def check_supabase_config():
    """Verifica as configurações do Supabase"""
    print("🔍 VERIFICANDO CONFIGURAÇÕES DO SUPABASE")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    print("📋 Variáveis de ambiente:")
    print(f"   SUPABASE_URL: {os.getenv('SUPABASE_URL', 'NÃO DEFINIDA')[:50]}...")
    print(f"   SUPABASE_KEY: {'DEFINIDA' if os.getenv('SUPABASE_KEY') else 'NÃO DEFINIDA'}")
    print(f"   SUPABASE_SERVICE_KEY: {'DEFINIDA' if os.getenv('SUPABASE_SERVICE_KEY') else 'NÃO DEFINIDA'}")
    print(f"   DATABASE_URL: {'DEFINIDA' if os.getenv('DATABASE_URL') else 'NÃO DEFINIDA'}")
    
    print("\n⚙️ Configurações do Django:")
    print(f"   SUPABASE_URL: {settings.SUPABASE_URL[:50]}...")
    print(f"   SUPABASE_KEY: {'DEFINIDA' if settings.SUPABASE_KEY else 'NÃO DEFINIDA'}")
    print(f"   SUPABASE_SERVICE_KEY: {'DEFINIDA' if settings.SUPABASE_SERVICE_KEY else 'NÃO DEFINIDA'}")
    print(f"   SUPABASE_STORAGE_BUCKET: {settings.SUPABASE_STORAGE_BUCKET}")
    
    # Testar upload
    print("\n🧪 Testando upload...")
    try:
        from loja.supabase_direct import upload_image_to_supabase
        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image
        import io
        
        # Criar imagem de teste
        img = Image.new('RGB', (50, 50), color='green')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        test_file = SimpleUploadedFile(
            "test_config.jpg",
            img_byte_arr.getvalue(),
            content_type="image/jpeg"
        )
        
        result = upload_image_to_supabase(test_file, "test")
        
        if result['success']:
            print("✅ Upload funcionou!")
            print(f"   URL: {result['public_url']}")
            return True
        else:
            print(f"❌ Erro no upload: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_supabase_config()
    if success:
        print("\n🎉 Configuração OK!")
    else:
        print("\n💥 Problema na configuração!")
        sys.exit(1)