"""
Upload direto para Supabase usando requests
Solução simples e robusta
"""
import requests
import uuid
import os
from PIL import Image
import io

# Configurações fixas do Supabase
SUPABASE_URL = "https://ubasgcbrwjdbhtxandrm.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViYXNnY2Jyd2pkYmh0eGFuZHJtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc3NjY2OTAsImV4cCI6MjA3MzM0MjY5MH0.jOWVQq_Yrl0LkFLj2IK2B0l1aHv2Pl5dxgne944eq5o"
BUCKET_NAME = "roupas"

def upload_image_to_supabase(image_file, folder_name="roupas"):
    """
    Upload direto para Supabase Storage
    """
    try:
        print(f"🚀 UPLOAD DIRETO PARA SUPABASE")
        print(f"   URL: {SUPABASE_URL}")
        print(f"   Bucket: {BUCKET_NAME}")
        
        # Gerar nome único para o arquivo
        if hasattr(image_file, 'name') and image_file.name:
            file_extension = os.path.splitext(image_file.name)[1].lower()
        else:
            file_extension = '.jpg'
        
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        storage_path = f"{folder_name}/{unique_filename}"
        
        # Processar imagem
        image_file.seek(0)
        image_data = image_file.read()
        
        # Redimensionar se necessário
        try:
            image = Image.open(io.BytesIO(image_data))
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Redimensionar se muito grande
            max_size = (1920, 1080)
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Converter para bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=85)
            image_data = img_byte_arr.getvalue()
            print(f"✅ Imagem processada: {image.size[0]}x{image.size[1]}")
        except Exception as e:
            print(f"⚠️  Usando dados originais: {e}")
        
        # Fazer upload via API REST do Supabase
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{storage_path}"
        
        headers = {
            'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
            'Content-Type': 'image/jpeg',
            'Cache-Control': 'max-age=3600'
        }
        
        print(f"🔗 Upload para: {upload_url}")
        
        response = requests.post(upload_url, data=image_data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Gerar URL pública
            public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{storage_path}"
            
            print(f"✅ Upload realizado com sucesso!")
            print(f"   URL pública: {public_url}")
            
            return {
                'success': True,
                'public_url': public_url,
                'storage_path': storage_path,
                'error': None
            }
        else:
            print(f"❌ Erro no upload: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
            return {
                'success': False,
                'error': f"Erro HTTP {response.status_code}: {response.text}",
                'public_url': None,
                'storage_path': None
            }
            
    except Exception as e:
        print(f"❌ Erro geral no upload: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'success': False,
            'error': f"Erro no upload: {str(e)}",
            'public_url': None,
            'storage_path': None
        }

def delete_image_from_supabase(storage_path):
    """
    Deletar imagem do Supabase Storage
    """
    try:
        if not storage_path:
            return {'success': True, 'error': None}
        
        delete_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{storage_path}"
        
        headers = {
            'Authorization': f'Bearer {SUPABASE_ANON_KEY}'
        }
        
        print(f"🗑️  Deletando: {delete_url}")
        
        response = requests.delete(delete_url, headers=headers, timeout=30)
        
        if response.status_code in [200, 204]:
            print(f"✅ Imagem deletada com sucesso!")
            return {'success': True, 'error': None}
        else:
            print(f"⚠️  Erro ao deletar: {response.status_code}")
            return {
                'success': False,
                'error': f"Erro HTTP {response.status_code}: {response.text}"
            }
            
    except Exception as e:
        print(f"❌ Erro ao deletar: {e}")
        return {
            'success': False,
            'error': f"Erro ao deletar: {str(e)}"
        }

def test_supabase_connection():
    """
    Testa a conexão com o Supabase
    """
    try:
        print("🧪 TESTANDO CONEXÃO COM SUPABASE")
        
        # Testar listagem de buckets
        list_url = f"{SUPABASE_URL}/storage/v1/bucket"
        headers = {
            'Authorization': f'Bearer {SUPABASE_ANON_KEY}'
        }
        
        response = requests.get(list_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            buckets = response.json()
            print(f"✅ Conexão funcionando! Buckets: {len(buckets)}")
            
            # Verificar se bucket 'roupas' existe
            bucket_names = [bucket.get('name', '') for bucket in buckets]
            if 'roupas' in bucket_names:
                print("✅ Bucket 'roupas' encontrado!")
                return True
            else:
                print(f"❌ Bucket 'roupas' não encontrado. Disponíveis: {bucket_names}")
                return False
        else:
            print(f"❌ Erro na conexão: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
