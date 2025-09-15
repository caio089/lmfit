#!/usr/bin/env python
"""
Teste simples do Supabase
Execute: python test_supabase.py
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
        from loja.supabase_direct import test_supabase_connection, upload_image_to_supabase
        
        # Testar conexão
        if test_supabase_connection():
            print("✅ Conexão com Supabase funcionando!")
            
            # Testar upload (com arquivo fake)
            from io import BytesIO
            from PIL import Image
            
            # Criar imagem de teste
            img = Image.new('RGB', (100, 100), color='red')
            img_byte = BytesIO()
            img.save(img_byte, format='JPEG')
            img_byte.seek(0)
            
            # Simular arquivo Django
            class FakeFile:
                def __init__(self, data):
                    self.data = data
                    self.name = 'test.jpg'
                
                def read(self):
                    return self.data
                
                def seek(self, pos):
                    pass
            
            fake_file = FakeFile(img_byte.getvalue())
            
            result = upload_image_to_supabase(fake_file, "test")
            
            if result['success']:
                print("✅ Upload de teste funcionando!")
                print(f"   URL: {result['public_url']}")
            else:
                print(f"❌ Erro no upload: {result['error']}")
        else:
            print("❌ Conexão com Supabase falhou!")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_supabase()
