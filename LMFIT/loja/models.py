from django.db import models
from django.contrib.auth.models import User

class Roupa(models.Model):
    CATEGORIA_CHOICES = [
        ('tops', 'Tops'),
        ('leggings', 'Leggings'),
        ('conjuntos', 'Conjuntos'),
        ('blusas', 'Blusas'),
        ('calcinha-sem-costura', 'Calcinha Sem Costura'),
        ('meias', 'Meias'),
        ('acessorios', 'Acessórios'),
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
    foto_principal = models.ImageField(upload_to='roupas/', verbose_name="Foto Principal")
    foto_2 = models.ImageField(upload_to='roupas/', blank=True, null=True, verbose_name="Foto 2")
    foto_3 = models.ImageField(upload_to='roupas/', blank=True, null=True, verbose_name="Foto 3")
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

class AdminUser(models.Model):
    """Modelo simples para autenticação do admin"""
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # Em produção, usar hash
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
