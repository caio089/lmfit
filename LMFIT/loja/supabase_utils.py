"""
Utilitários para integração com Supabase Storage
"""
import os
import uuid
from django.conf import settings
from PIL import Image
import io

# Cliente Supabase será inicializado quando necessário
_supabase_client = None

def get_supabase_client():
    """Inicializa o cliente Supabase apenas quando necessário"""
    global _supabase_client
    if _supabase_client is None:
        try:
            # Verificar se as variáveis estão definidas
            if not hasattr(settings, 'SUPABASE_URL') or not settings.SUPABASE_URL:
                print("❌ SUPABASE_URL não definida no settings.py")
                return None
                
            if not hasattr(settings, 'SUPABASE_SERVICE_KEY') or not settings.SUPABASE_SERVICE_KEY:
                print("❌ SUPABASE_SERVICE_KEY não definida no settings.py")
                return None
            
            # Importar e criar cliente
            from supabase import create_client
            
            print(f"🔗 Conectando ao Supabase: {settings.SUPABASE_URL}")
            print(f"🔑 Usando bucket: {settings.SUPABASE_STORAGE_BUCKET}")
            
            _supabase_client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_KEY
            )
            
            print("✅ Cliente Supabase inicializado com sucesso!")
            
        except ImportError as e:
            print(f"❌ Supabase não instalado: {e}")
            print("💡 Execute: pip install supabase==2.0.2")
            return None
        except Exception as e:
            print(f"❌ Erro ao inicializar Supabase: {e}")
            import traceback
            traceback.print_exc()
            return None
    return _supabase_client

def upload_image_to_supabase(image_file, folder_name="general"):
    """
    Faz upload de uma imagem para o Supabase Storage
    
    Args:
        image_file: Arquivo de imagem do Django
        folder_name: Nome da pasta no storage
        
    Returns:
        dict: {'success': bool, 'public_url': str, 'storage_path': str, 'error': str}
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return {
                'success': False,
                'error': 'Cliente Supabase não disponível',
                'public_url': None,
                'storage_path': None
            }
        
        # Gerar nome único para o arquivo
        file_extension = os.path.splitext(image_file.name)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        storage_path = f"{folder_name}/{unique_filename}"
        
        # Otimizar imagem se necessário
        image = Image.open(image_file)
        
        # Redimensionar se muito grande (max 1920x1080)
        max_size = (1920, 1080)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Converter para bytes
        img_byte_arr = io.BytesIO()
        image_format = image.format if image.format else 'JPEG'
        image.save(img_byte_arr, format=image_format, quality=85)
        img_byte_arr = img_byte_arr.getvalue()
        
        # Fazer upload para Supabase Storage
        try:
            result = supabase.storage.from_(settings.SUPABASE_STORAGE_BUCKET).upload(
                storage_path,
                img_byte_arr
            )
        except Exception as upload_error:
            return {
                'success': False,
                'error': f"Erro no upload: {str(upload_error)}",
                'public_url': None,
                'storage_path': None
            }
        
        # Verificar se houve erro no upload
        if isinstance(result, dict) and 'error' in result:
            return {
                'success': False,
                'error': f"Erro no upload: {result['error']}",
                'public_url': None,
                'storage_path': None
            }
        
        # Gerar URL pública
        public_url = supabase.storage.from_(settings.SUPABASE_STORAGE_BUCKET).get_public_url(storage_path)
        
        return {
            'success': True,
            'public_url': public_url,
            'storage_path': storage_path,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Erro ao processar imagem: {str(e)}",
            'public_url': None,
            'storage_path': None
        }

def delete_image_from_supabase(storage_path):
    """
    Deleta uma imagem do Supabase Storage
    
    Args:
        storage_path: Caminho da imagem no storage
        
    Returns:
        dict: {'success': bool, 'error': str}
    """
    try:
        if not storage_path:
            return {'success': True, 'error': None}
        
        supabase = get_supabase_client()
        if not supabase:
            return {
                'success': False,
                'error': 'Cliente Supabase não disponível'
            }
            
        result = supabase.storage.from_(settings.SUPABASE_STORAGE_BUCKET).remove([storage_path])
        
        # Verificar se houve erro na deleção
        if isinstance(result, dict) and 'error' in result:
            return {
                'success': False,
                'error': f"Erro ao deletar: {result['error']}"
            }
        
        return {'success': True, 'error': None}
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Erro ao deletar imagem: {str(e)}"
        }
