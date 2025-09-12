from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Cria ou atualiza o usuário admin com senha luara10'

    def handle(self, *args, **options):
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
        
        self.stdout.write(
            self.style.SUCCESS('🌐 Acesse: https://seu-app.onrender.com/admin/')
        )
