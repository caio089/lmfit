import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from django.contrib.auth.models import User

print("🔐 ALTERANDO SENHA DO ADMIN...")
print("=" * 40)

try:
    # Buscar usuário admin
    user = User.objects.get(username='admin')
    
    # Alterar email e senha
    user.email = 'luaracarvalho10@icloud.com'
    user.set_password('luara10')
    user.save()
    
    print("✅ SENHA ALTERADA COM SUCESSO!")
    print("👤 Usuário: admin")
    print("📧 Email: luaracarvalho10@icloud.com")
    print("🔑 Senha: luara10")
    print("\n🌐 Acesse: http://127.0.0.1:8000/admin/")
    
except User.DoesNotExist:
    print("❌ Usuário 'admin' não encontrado!")
    print("Criando novo usuário...")
    
    # Criar novo usuário admin
    user = User.objects.create_superuser(
        username='admin',
        email='luaracarvalho10@icloud.com',
        password='luara10'
    )
    
    print("✅ NOVO USUÁRIO ADMIN CRIADO!")
    print("👤 Usuário: admin")
    print("📧 Email: luaracarvalho10@icloud.com")
    print("🔑 Senha: luara10")
    
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n🚀 Pronto! Agora você pode acessar o painel!")
