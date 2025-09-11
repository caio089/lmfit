from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.models import CloudinaryField

class Roupa(models.Model):
    CATEGORIA_CHOICES = [
        ('tops', 'Tops'),
        ('leggings', 'Leggings'),
        ('conjuntos', 'Conjuntos'),
        ('blusas', 'Blusas'),
        ('acessorios', 'Acessórios'),
        ('macacao', 'Macacão'),
        ('macaquinho', 'Macaquinho'),
        ('short', 'Short'),
        ('regata', 'Regata'),
    ]
    
    TAMANHO_CHOICES = [
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name="Nome da Roupa")
    descricao = models.TextField(verbose_name="Descrição")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, verbose_name="Categoria")
    tamanhos_disponiveis = models.CharField(max_length=20, default="P,M,G", verbose_name="Tamanhos Disponíveis")
    foto_principal = CloudinaryField(verbose_name="Foto Principal")
    foto_2 = CloudinaryField(blank=True, null=True, verbose_name="Foto 2")
    foto_3 = CloudinaryField(blank=True, null=True, verbose_name="Foto 3")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    
    class Meta:
        verbose_name = "Roupa"
        verbose_name_plural = "Roupas"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return self.nome
    
    def get_tamanhos_list(self):
        """Retorna lista dos tamanhos disponíveis"""
        return [t.strip() for t in self.tamanhos_disponiveis.split(',')]
    
    def get_foto_principal_url(self):
        """Retorna URL da foto principal do Cloudinary"""
        if self.foto_principal:
            return self.foto_principal.url
        return None
    
    def get_foto_2_url(self):
        """Retorna URL da foto 2 do Cloudinary"""
        if self.foto_2:
            return self.foto_2.url
        return None
    
    def get_foto_3_url(self):
        """Retorna URL da foto 3 do Cloudinary"""
        if self.foto_3:
            return self.foto_3.url
        return None

class AdminUser(models.Model):
    """Modelo simples para autenticação do admin"""
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # Em produção, usar hash
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
