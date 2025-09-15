#!/usr/bin/env python
import os
import django

# Configurar Django PRIMEIRO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

# Agora importar após setup
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from loja.views import admin_roupa_add
from PIL import Image
import io

print("=== TESTANDO UPLOAD DO PAINEL ===")

# Criar uma imagem de teste
img = Image.new('RGB', (400, 500), color='lightblue')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

# Criar arquivo como seria enviado pelo formulário
image_file = SimpleUploadedFile(
    "teste_roupa.jpg",
    img_bytes.getvalue(),
    content_type="image/jpeg"
)

# Criar request factory
factory = RequestFactory()

# Simular dados do formulário
post_data = {
    'nome': 'Teste Roupa Painel',
    'descricao': 'Roupa de teste criada pelo painel',
    'preco': '99.90',
    'categoria': 'leggings',
    'tamanhos_disponiveis': 'P,M,G',
    'ativo': 'on'
}

# Criar request POST
request = factory.post('/painel/roupas/add/', post_data)
request.FILES['foto_principal'] = image_file

# Criar usuário admin para o teste
try:
    user = User.objects.get(username='admin')
    request.user = user
    print(f"✅ Usuário admin encontrado: {user.username}")
except User.DoesNotExist:
    print("❌ Usuário admin não encontrado")
    exit(1)

# Testar a view
try:
    print("🔄 Testando upload via painel...")
    response = admin_roupa_add(request)
    print(f"✅ Resposta: {response.status_code}")
    print(f"✅ Tipo de resposta: {type(response)}")
except Exception as e:
    print(f"❌ Erro na view: {e}")
    import traceback
    traceback.print_exc()
