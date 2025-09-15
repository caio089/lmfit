from django.contrib.auth import get_user_model

class EnsureAdminUserMiddleware:
    """Middleware que garante que o usuário admin existe"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_created = False

    def __call__(self, request):
        # Só criar o admin uma vez por instância do middleware
        if not self.admin_created:
            try:
                User = get_user_model()
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser(
                        username='admin',
                        email='admin@lmfit.com',
                        password='luara10'
                    )
                    print("✅ Usuário admin criado automaticamente via middleware")
                self.admin_created = True
            except Exception as e:
                print(f"❌ Erro ao criar usuário admin no middleware: {e}")

        response = self.get_response(request)
        return response
