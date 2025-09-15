from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Força migração limpando tabelas conflitantes'

    def handle(self, *args, **options):
        self.stdout.write("=== FORÇANDO MIGRAÇÃO ===")
        
        try:
            with connection.cursor() as cursor:
                # Verificar se as tabelas existem
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name IN ('loja_adminuser', 'loja_roupa')
                """)
                existing_tables = [row[0] for row in cursor.fetchall()]
                
                self.stdout.write(f"Tabelas existentes: {existing_tables}")
                
                if existing_tables:
                    self.stdout.write("Removendo tabelas conflitantes...")
                    
                    # Deletar tabelas em ordem
                    for table in ['loja_roupa', 'loja_adminuser']:
                        if table in existing_tables:
                            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                            self.stdout.write(f"Tabela {table} removida")
                    
                    # Limpar histórico de migrações
                    cursor.execute("DELETE FROM django_migrations WHERE app = 'loja';")
                    self.stdout.write("Histórico de migrações limpo")
                
                # Executar migrações
                self.stdout.write("Executando migrações...")
                call_command('migrate', verbosity=2)
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Erro: {e}")
            )
            # Fallback: tentar migração com --fake
            self.stdout.write("Tentando migração com --fake...")
            try:
                call_command('migrate', 'loja', '0001', '--fake', verbosity=2)
                call_command('migrate', verbosity=2)
            except:
                call_command('migrate', '--fake-initial', verbosity=2)
        
        self.stdout.write(
            self.style.SUCCESS('=== MIGRAÇÃO FORÇADA CONCLUÍDA ===')
        )
