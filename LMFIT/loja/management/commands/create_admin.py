from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
import os

class Command(BaseCommand):
    help = 'Cria usuário admin com credenciais fixas'

    def handle(self, *args, **options):
        self.stdout.write("=== CRIANDO USUÁRIO ADMIN ===")
        
        try:
            User = get_user_model()
            
            with transaction.atomic():
                # Deletar usuário admin existente se houver
                User.objects.filter(username='admin').delete()
                self.stdout.write("Usuário admin anterior removido (se existia)")
                
                # Criar novo usuário admin
                user = User.objects.create_superuser(
                    username='admin',
                    email='admin@lmfit.com',
                    password='luara10',
                    first_name='Admin',
                    last_name='LMFIT'
                )
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Usuário admin criado com sucesso!')
                )
                self.stdout.write(f'👤 Usuário: admin')
                self.stdout.write(f'🔑 Senha: luara10')
                self.stdout.write(f'📧 Email: admin@lmfit.com')
                
                # Verificar se o usuário foi criado
                if User.objects.filter(username='admin').exists():
                    self.stdout.write('✅ Verificação: Usuário existe no banco')
                    
                    # Testar login
                    from django.contrib.auth import authenticate
                    test_user = authenticate(username='admin', password='luara10')
                    if test_user:
                        self.stdout.write('✅ Verificação: Login funciona corretamente')
                    else:
                        self.stdout.write('❌ Erro: Login não funciona')
                else:
                    self.stdout.write('❌ Erro: Usuário não foi criado')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao criar admin: {str(e)}')
            )
            import traceback
            self.stdout.write(f'Traceback: {traceback.format_exc()}')
        
        self.stdout.write("=== FIM DA CRIAÇÃO ===")
