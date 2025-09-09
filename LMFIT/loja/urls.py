from django.urls import path
from .views import (
    loja, 
    admin_login, 
    admin_logout, 
    admin_dashboard, 
    admin_roupas_list, 
    admin_roupa_add, 
    admin_roupa_edit, 
    admin_roupa_delete, 
    admin_roupa_toggle_status
)

urlpatterns = [
    # Página principal da loja
    path('', loja, name='loja'),
    
    # URLs da área administrativa
    path('painel/', admin_login, name='admin_login'),
    path('painel/logout/', admin_logout, name='admin_logout'),
    path('painel/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('painel/roupas/', admin_roupas_list, name='admin_roupas_list'),
    path('painel/roupas/add/', admin_roupa_add, name='admin_roupa_add'),
    path('painel/roupas/edit/<int:roupa_id>/', admin_roupa_edit, name='admin_roupa_edit'),
    path('painel/roupas/delete/<int:roupa_id>/', admin_roupa_delete, name='admin_roupa_delete'),
    path('painel/roupas/toggle/<int:roupa_id>/', admin_roupa_toggle_status, name='admin_roupa_toggle_status'),
]