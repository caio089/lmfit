#!/usr/bin/env python
"""
Script para migrar dados do SQLite local para PostgreSQL no Render
Execute este script ANTES de fazer deploy para preservar os dados
"""

import os
import sys
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.models import Roupa
from django.contrib.auth.models import User

def export_data():
    """Exporta dados do SQLite local para JSON"""
    print("📤 Exportando dados do banco local...")
    
    try:
        # Exportar roupas
        roupas_data = []
        for roupa in Roupa.objects.all():
            roupas_data.append({
                'nome': roupa.nome,
                'descricao': roupa.descricao,
                'preco': float(roupa.preco),
                'categoria': roupa.categoria,
                'tamanhos_disponiveis': roupa.tamanhos_disponiveis,
                'foto_principal': roupa.foto_principal.decode('latin-1') if roupa.foto_principal else None,
                'foto_2': roupa.foto_2.decode('latin-1') if roupa.foto_2 else None,
                'foto_3': roupa.foto_3.decode('latin-1') if roupa.foto_3 else None,
                'ativo': roupa.ativo,
                'data_criacao': roupa.data_criacao.isoformat(),
                'data_atualizacao': roupa.data_atualizacao.isoformat(),
            })
        
        # Salvar em arquivo JSON
        with open('dados_exportados.json', 'w', encoding='utf-8') as f:
            json.dump(roupas_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(roupas_data)} roupas exportadas para 'dados_exportados.json'")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao exportar dados: {e}")
        return False

def import_data():
    """Importa dados do JSON para o banco atual"""
    print("📥 Importando dados do arquivo JSON...")
    
    try:
        # Ler arquivo JSON
        with open('dados_exportados.json', 'r', encoding='utf-8') as f:
            roupas_data = json.load(f)
        
        # Importar roupas
        for data in roupas_data:
            # Verificar se já existe
            if not Roupa.objects.filter(nome=data['nome']).exists():
                roupa = Roupa.objects.create(
                    nome=data['nome'],
                    descricao=data['descricao'],
                    preco=data['preco'],
                    categoria=data['categoria'],
                    tamanhos_disponiveis=data['tamanhos_disponiveis'],
                    ativo=data['ativo'],
                )
                
                # Restaurar fotos
                if data['foto_principal']:
                    roupa.foto_principal = data['foto_principal'].encode('latin-1')
                if data['foto_2']:
                    roupa.foto_2 = data['foto_2'].encode('latin-1')
                if data['foto_3']:
                    roupa.foto_3 = data['foto_3'].encode('latin-1')
                
                roupa.save()
                print(f"✅ Importada: {data['nome']}")
            else:
                print(f"⚠️ Já existe: {data['nome']}")
        
        print(f"✅ Importação concluída! {len(roupas_data)} roupas processadas")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao importar dados: {e}")
        return False

def main():
    """Função principal"""
    print("🔄 MIGRAÇÃO DE DADOS SQLITE → POSTGRESQL")
    print("=" * 50)
    
    # Verificar se estamos no Render
    if os.getenv("RENDER"):
        print("🌐 Executando no Render - importando dados...")
        success = import_data()
    else:
        print("🏠 Executando localmente - exportando dados...")
        success = export_data()
    
    if success:
        print("\n✅ Migração concluída com sucesso!")
        print("📝 Agora você pode fazer deploy com segurança!")
    else:
        print("\n❌ Falha na migração. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()
