#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMFIT.settings')
django.setup()

from loja.models import Roupa

print("=== TESTANDO SALVAMENTO DE ROUPA ===")

# Criar uma roupa de teste
try:
    roupa = Roupa(
        nome="Legging Teste",
        descricao="Legging de teste para verificar se o banco está funcionando",
        preco=89.90,
        categoria="leggings",
        tamanhos_disponiveis="P,M,G",
        foto_principal="https://exemplo.com/teste.jpg",
        ativo=True
    )
    
    roupa.save()
    print("✅ Roupa salva com sucesso!")
    print(f"ID: {roupa.id}")
    print(f"Nome: {roupa.nome}")
    
    # Verificar se foi salva
    total = Roupa.objects.count()
    print(f"Total de roupas no banco: {total}")
    
except Exception as e:
    print(f"❌ Erro ao salvar roupa: {e}")
    import traceback
    traceback.print_exc()
