import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.models import AdminUser

# Criar usuário administrador
admin_user, created = AdminUser.objects.get_or_create(
    username='admin',
    defaults={
        'password': '123',
        'nome': 'Administrador',
        'ativo': True
    }
)

if created:
    print('✅ Usuário administrador criado com sucesso!')
    print('👤 Usuário: admin')
    print('🔑 Senha: admin123')
else:
    print('ℹ️ Usuário administrador já existe!')
    print('👤 Usuário: admin')
    print('🔑 Senha: admin123')
