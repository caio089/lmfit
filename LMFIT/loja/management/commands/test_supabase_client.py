from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Testa o cliente Supabase'

    def handle(self, *args, **options):
        self.stdout.write("=== TESTE DO CLIENTE SUPABASE ===")
        
        try:
            from loja.supabase_utils import get_supabase_client
            
            self.stdout.write("Importando cliente...")
            client = get_supabase_client()
            
            if client:
                self.stdout.write(self.style.SUCCESS("✅ Cliente Supabase criado com sucesso!"))
                self.stdout.write(f"Tipo do cliente: {type(client)}")
                
                # Testar operação básica
                try:
                    buckets = client.storage.list_buckets()
                    self.stdout.write(self.style.SUCCESS("✅ Conexão com Supabase funcionando!"))
                    self.stdout.write(f"Buckets encontrados: {len(buckets)}")
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"⚠️  Cliente criado mas erro na operação: {e}"))
            else:
                self.stdout.write(self.style.ERROR("❌ Cliente retornou None"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erro: {e}"))
            import traceback
            traceback.print_exc()
        
        self.stdout.write("=== FIM DO TESTE ===")
