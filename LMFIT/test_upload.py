#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.supabase_utils import upload_image_to_supabase

# Criar um arquivo de teste que simula um arquivo Django real
class DjangoFile:
    def __init__(self, data, name):
        self.name = name
        self._data = data
        self._position = 0
    
    def read(self):
        return self._data
    
    def seek(self, position):
        self._position = position

# Testar com dados de uma imagem real (JPEG header)
# Criar um JPEG minimal válido
jpeg_header = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'

test_file = DjangoFile(jpeg_header, "test.jpg")

print("=== TESTANDO UPLOAD COM IMAGEM JPEG ===")
result = upload_image_to_supabase(test_file, "test")
print(f"Resultado: {result}")

