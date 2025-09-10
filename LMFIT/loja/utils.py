from PIL import Image
import io
from django.core.files.base import ContentFile

def convert_to_webp(image_file, quality=85, max_width=800):
    """
    Converte uma imagem para WebP e redimensiona se necessário
    
    Args:
        image_file: Arquivo de imagem (UploadedFile ou similar)
        quality: Qualidade da compressão WebP (0-100)
        max_width: Largura máxima da imagem
    
    Returns:
        ContentFile: Arquivo WebP convertido
    """
    try:
        # Abrir a imagem
        image = Image.open(image_file)
        
        # Converter para RGB se necessário (WebP não suporta RGBA)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Criar fundo branco para imagens com transparência
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionar se necessário
        if image.width > max_width:
            ratio = max_width / image.width
            new_height = int(image.height * ratio)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Converter para WebP
        output = io.BytesIO()
        image.save(output, format='WebP', quality=quality, optimize=True)
        output.seek(0)
        
        # Criar ContentFile
        filename = image_file.name.rsplit('.', 1)[0] + '.webp'
        return ContentFile(output.getvalue(), name=filename)
        
    except Exception as e:
        print(f"Erro ao converter imagem para WebP: {e}")
        # Se der erro, retorna o arquivo original
        return image_file

def get_image_data_url(image_binary):
    """
    Converte dados binários de imagem para data URL (base64)
    
    Args:
        image_binary: Dados binários da imagem
    
    Returns:
        str: Data URL da imagem
    """
    import base64
    
    if image_binary:
        # Converter para base64
        image_base64 = base64.b64encode(image_binary).decode('utf-8')
        return f"data:image/webp;base64,{image_base64}"
    return None