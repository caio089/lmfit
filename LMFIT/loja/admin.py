from django.contrib import admin
from .models import Roupa, AdminUser

@admin.register(Roupa)
class RoupaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'ativo', 'data_criacao']
    list_filter = ['categoria', 'ativo', 'data_criacao']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo']
    ordering = ['-data_criacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'categoria', 'preco', 'tamanhos_disponiveis')
        }),
        ('Fotos', {
            'fields': ('foto_principal', 'foto_principal_storage_path', 'foto_2', 'foto_2_storage_path', 'foto_3', 'foto_3_storage_path')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )
    
    readonly_fields = ['data_criacao', 'data_atualizacao']

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'nome', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'data_criacao']
    search_fields = ['username', 'nome']
    list_editable = ['ativo']
