# Generated manually for safe migration

from django.db import migrations, connection

def check_and_create_tables(apps, schema_editor):
    """Verifica se as tabelas existem antes de criá-las"""
    with connection.cursor() as cursor:
        # Verificar se loja_adminuser existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'loja_adminuser'
            );
        """)
        adminuser_exists = cursor.fetchone()[0]
        
        # Verificar se loja_roupa existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'loja_roupa'
            );
        """)
        roupa_exists = cursor.fetchone()[0]
        
        if not adminuser_exists:
            cursor.execute("""
                CREATE TABLE loja_adminuser (
                    id BIGSERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    nome VARCHAR(100) NOT NULL,
                    ativo BOOLEAN DEFAULT TRUE NOT NULL,
                    data_criacao TIMESTAMPTZ DEFAULT NOW() NOT NULL
                );
            """)
        
        if not roupa_exists:
            cursor.execute("""
                CREATE TABLE loja_roupa (
                    id BIGSERIAL PRIMARY KEY,
                    nome VARCHAR(200) NOT NULL,
                    descricao TEXT NOT NULL,
                    preco DECIMAL(10,2) NOT NULL,
                    categoria VARCHAR(50) NOT NULL,
                    tamanhos_disponiveis VARCHAR(20) DEFAULT 'P,M,G' NOT NULL,
                    foto_principal VARCHAR(500) NOT NULL,
                    foto_principal_storage_path VARCHAR(200),
                    foto_2 VARCHAR(500),
                    foto_2_storage_path VARCHAR(200),
                    foto_3 VARCHAR(500),
                    foto_3_storage_path VARCHAR(200),
                    ativo BOOLEAN DEFAULT TRUE NOT NULL,
                    data_criacao TIMESTAMPTZ DEFAULT NOW() NOT NULL,
                    data_atualizacao TIMESTAMPTZ DEFAULT NOW() NOT NULL
                );
            """)

def reverse_check_and_create_tables(apps, schema_editor):
    """Reverter a migração"""
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS loja_roupa CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS loja_adminuser CASCADE;")

class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(check_and_create_tables, reverse_check_and_create_tables),
    ]
