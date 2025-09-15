from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Testa as variáveis de ambiente do Supabase'

    def handle(self, *args, **options):
        self.stdout.write("=== TESTE DAS VARIÁVEIS DE AMBIENTE ===")
        
        # Testar variáveis do ambiente
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
        supabase_bucket = os.getenv("SUPABASE_STORAGE_BUCKET")
        
        self.stdout.write(f"SUPABASE_URL: {supabase_url}")
        self.stdout.write(f"SUPABASE_KEY: {'DEFINIDA' if supabase_key else 'NÃO DEFINIDA'}")
        self.stdout.write(f"SUPABASE_SERVICE_KEY: {'DEFINIDA' if supabase_service_key else 'NÃO DEFINIDA'}")
        self.stdout.write(f"SUPABASE_STORAGE_BUCKET: {supabase_bucket}")
        
        # Testar criação do cliente
        try:
            from supabase import create_client
            
            if supabase_url and supabase_key:
                client = create_client(supabase_url, supabase_key)
                self.stdout.write(self.style.SUCCESS("✅ Cliente Supabase criado com sucesso!"))
                
                # Testar conexão
                try:
                    # Tentar listar buckets
                    buckets = client.storage.list_buckets()
                    self.stdout.write(self.style.SUCCESS("✅ Conexão com Supabase funcionando!"))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"⚠️  Cliente criado mas erro na conexão: {e}"))
            else:
                self.stdout.write(self.style.ERROR("❌ Variáveis não definidas"))
                
        except ImportError:
            self.stdout.write(self.style.ERROR("❌ Supabase não instalado"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erro ao criar cliente: {e}"))
        
        self.stdout.write("=== FIM DO TESTE ===")
