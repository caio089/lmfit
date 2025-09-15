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
            # Ler variáveis diretamente do ambiente
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")  # Usar chave anon para uploads
            supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
            
            print(f"🔍 DEBUG VARIÁVEIS DE AMBIENTE:")
            print(f"   SUPABASE_URL: {supabase_url[:50]}..." if supabase_url else "   SUPABASE_URL: None")
            print(f"   SUPABASE_KEY: {'DEFINIDA' if supabase_key else 'None'}")
            print(f"   SUPABASE_SERVICE_KEY: {'DEFINIDA' if supabase_service_key else 'None'}")
            
            # Verificar se as variáveis estão definidas
            if not supabase_url:
                print("❌ SUPABASE_URL não definida no ambiente")
                return None
                
            if not supabase_key:
                print("❌ SUPABASE_KEY não definida no ambiente")
                return None
            
            # Importar e criar cliente
            from supabase import create_client
            
            print(f"🔗 Conectando ao Supabase: {supabase_url}")
            print(f"🔑 Usando chave: {'ANON' if supabase_key else 'SERVICE'}")
            
            # Usar chave anon para uploads (mais seguro)
            _supabase_client = create_client(
                supabase_url,
                supabase_key  # Usar chave anon em vez de service key
            )
            
            print("✅ Cliente Supabase inicializado com sucesso!")
            
        except ImportError as e:
            print(f"❌ Supabase não instalado: {e}")
            print("💡 Execute: pip install supabase==2.0.2")
            return None
        except Exception as e:
            print(f"❌ Erro ao inicializar Supabase: {e}")
            print(f"❌ DEBUG: SUPABASE_URL = {os.getenv('SUPABASE_URL', 'NÃO DEFINIDA')}")
            print(f"❌ DEBUG: SUPABASE_KEY = {os.getenv('SUPABASE_KEY', 'NÃO DEFINIDA')}")
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
            print("❌ DEBUG: Cliente Supabase retornou None")
            return {
                'success': False,
                'error': 'Cliente Supabase não disponível - verifique as configurações',
                'public_url': None,
                'storage_path': None
            }
        
        # Gerar nome único para o arquivo
        if hasattr(image_file, 'name') and image_file.name:
            file_extension = os.path.splitext(image_file.name)[1].lower()
        else:
            file_extension = '.jpg'  # Default para BytesIO
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        storage_path = f"{folder_name}/{unique_filename}"
        
        # Processar imagem
        try:
            # Para arquivos do Django, usar diretamente
            if hasattr(image_file, 'read'):
                # Arquivo Django - ler dados
                image_file.seek(0)
                image_data = image_file.read()
            elif hasattr(image_file, 'getvalue'):
                # BytesIO object
                image_data = image_file.getvalue()
            else:
                # Outros tipos de arquivo
                image_data = image_file
            
            # Verificar se é uma imagem válida
            try:
                image = Image.open(io.BytesIO(image_data))
                
                # Converter para RGB se necessário
                if image.mode in ('RGBA', 'LA', 'P'):
                    image = image.convert('RGB')
                
                # Redimensionar se muito grande (max 1920x1080)
                max_size = (1920, 1080)
                if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                    image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Converter para bytes
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG', quality=85)
                img_byte_arr = img_byte_arr.getvalue()
                
            except Exception as img_error:
                # Se não conseguir processar como imagem, usar dados originais
                print(f"⚠️  Não foi possível processar como imagem, usando dados originais: {img_error}")
                img_byte_arr = image_data
            
        except Exception as general_error:
            print(f"❌ DEBUG: Erro geral ao processar arquivo: {general_error}")
            print(f"❌ DEBUG: Tipo do arquivo: {type(image_file)}")
            print(f"❌ DEBUG: Nome do arquivo: {getattr(image_file, 'name', 'N/A')}")
            return {
                'success': False,
                'error': f'Erro ao processar arquivo: {str(general_error)}',
                'public_url': None,
                'storage_path': None
            }
        
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
