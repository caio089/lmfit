from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command
import sys

class Command(BaseCommand):
    help = 'Verifica o estado do banco de dados e executa migrações se necessário'

    def handle(self, *args, **options):
        self.stdout.write("=== INICIANDO VERIFICAÇÃO DO BANCO ===")
        
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
                
                if 'loja_adminuser' in existing_tables and 'loja_roupa' in existing_tables:
                    self.stdout.write(
                        self.style.WARNING(
                            "Tabelas já existem. Marcando migração inicial como aplicada..."
                        )
                    )
                    # Marcar a migração inicial como aplicada
                    call_command('migrate', 'loja', '0001', '--fake', verbosity=2)
                    # Executar outras migrações se houver
                    call_command('migrate', verbosity=2)
                else:
                    self.stdout.write("Executando migrações normalmente...")
                    call_command('migrate', verbosity=2)
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Erro ao verificar banco: {e}")
            )
            # Em caso de erro, tentar migração normal
            self.stdout.write("Tentando migração normal como fallback...")
            call_command('migrate', verbosity=2)
        
        self.stdout.write(
            self.style.SUCCESS('=== VERIFICAÇÃO DO BANCO CONCLUÍDA ===')
        )
