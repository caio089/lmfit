from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Cria ou atualiza o usuário admin com senha luara10'

    def handle(self, *args, **options):
        try:
            User = get_user_model()
            
            # Verificar se já existe
            if User.objects.filter(username='admin').exists():
                user = User.objects.get(username='admin')
                user.set_password('luara10')
                user.save()
                self.stdout.write(
                    self.style.SUCCESS('✅ Senha do usuário "admin" alterada para "luara10"')
                )
            else:
                User.objects.create_superuser(
                    username='admin',
                    email='admin@lmfit.com',
                    password='luara10'
                )
                self.stdout.write(
                    self.style.SUCCESS('✅ Superusuário "admin" criado com senha "luara10"')
                )
            
            # Obter URL do Render se disponível
            render_url = os.getenv('RENDER_EXTERNAL_URL', 'https://seu-app.onrender.com')
            self.stdout.write(
                self.style.SUCCESS(f'🌐 Acesse: {render_url}/admin/')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao criar/atualizar admin: {str(e)}')
            )
            # Log do erro para debug
            import traceback
            self.stdout.write(
                self.style.ERROR(f'Traceback: {traceback.format_exc()}')
            )
