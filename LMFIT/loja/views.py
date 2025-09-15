from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Roupa, AdminUser
from .supabase_utils import upload_image_to_supabase, delete_image_from_supabase
import json

def loja(request):
    try:
        # Buscar todas as roupas ativas
        roupas = Roupa.objects.filter(ativo=True).order_by('-data_criacao')
        return render(request, "loja/loja.html", {'roupas': roupas})
    except Exception as e:
        # Em caso de erro, retornar lista vazia
        return render(request, "loja/loja.html", {'roupas': []})

# ========== SISTEMA DE ADMINISTRAÇÃO ==========

def admin_login(request):
    """Página de login para administradores"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Usar autenticação padrão do Django
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser or user.is_staff:
                login(request, user)
                messages.success(request, f'Bem-vindo(a), {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Você não tem permissão para acessar esta área!')
        else:
            messages.error(request, 'Usuário ou senha incorretos!')
    
    return render(request, 'loja/admin/login.html')

def admin_logout(request):
    """Logout do administrador"""
    logout(request)
    messages.info(request, 'Você foi desconectado!')
    return redirect('admin_login')

def admin_required(view_func):
    """Decorator para verificar se o admin está logado"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'Você precisa fazer login para acessar esta área!')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_dashboard(request):
    """Dashboard principal do administrador"""
    total_roupas = Roupa.objects.count()
    roupas_ativas = Roupa.objects.filter(ativo=True).count()
    roupas_inativas = Roupa.objects.filter(ativo=False).count()
    
    context = {
        'total_roupas': total_roupas,
        'roupas_ativas': roupas_ativas,
        'roupas_inativas': roupas_inativas,
        'admin_name': request.user.username
    }
    return render(request, 'loja/admin/dashboard.html', context)

@admin_required
def admin_roupas_list(request):
    """Lista todas as roupas para administração"""
    roupas = Roupa.objects.all().order_by('-data_criacao')
    return render(request, 'loja/admin/roupas_list.html', {'roupas': roupas})

@admin_required
def admin_roupa_add(request):
    """Adicionar nova roupa"""
    if request.method == 'POST':
        try:
            # Criar nova roupa
            roupa = Roupa(
                nome=request.POST.get('nome'),
                descricao=request.POST.get('descricao'),
                preco=request.POST.get('preco'),
                categoria=request.POST.get('categoria'),
                tamanhos_disponiveis=request.POST.get('tamanhos_disponiveis'),
                ativo=request.POST.get('ativo') == 'on'
            )
            
            # Processar fotos - upload para Supabase Storage
            if 'foto_principal' in request.FILES and request.FILES['foto_principal']:
                upload_result = upload_image_to_supabase(
                    request.FILES['foto_principal'], 
                    folder_name="roupas"
                )
                if upload_result['success']:
                    roupa.foto_principal = upload_result['public_url']
                    roupa.foto_principal_storage_path = upload_result['storage_path']
                else:
                    messages.error(request, f'Erro ao fazer upload da foto principal: {upload_result["error"]}')
                    return render(request, 'loja/admin/roupa_form.html', {'action': 'add'})
            
            if 'foto_2' in request.FILES and request.FILES['foto_2']:
                upload_result = upload_image_to_supabase(
                    request.FILES['foto_2'], 
                    folder_name="roupas"
                )
                if upload_result['success']:
                    roupa.foto_2 = upload_result['public_url']
                    roupa.foto_2_storage_path = upload_result['storage_path']
                else:
                    messages.warning(request, f'Erro ao fazer upload da foto 2: {upload_result["error"]}')
            
            if 'foto_3' in request.FILES and request.FILES['foto_3']:
                upload_result = upload_image_to_supabase(
                    request.FILES['foto_3'], 
                    folder_name="roupas"
                )
                if upload_result['success']:
                    roupa.foto_3 = upload_result['public_url']
                    roupa.foto_3_storage_path = upload_result['storage_path']
                else:
                    messages.warning(request, f'Erro ao fazer upload da foto 3: {upload_result["error"]}')
            
            roupa.save()
            messages.success(request, f'Roupa "{roupa.nome}" adicionada com sucesso!')
            return redirect('admin_roupas_list')
            
        except Exception as e:
            messages.error(request, f'Erro ao adicionar roupa: {str(e)}')
    
    return render(request, 'loja/admin/roupa_form.html', {'action': 'add'})

@admin_required
def admin_roupa_edit(request, roupa_id):
    """Editar roupa existente"""
    roupa = get_object_or_404(Roupa, id=roupa_id)
    
    if request.method == 'POST':
        try:
            roupa.nome = request.POST.get('nome')
            roupa.descricao = request.POST.get('descricao')
            roupa.preco = request.POST.get('preco')
            roupa.categoria = request.POST.get('categoria')
            roupa.tamanhos_disponiveis = request.POST.get('tamanhos_disponiveis')
            roupa.ativo = request.POST.get('ativo') == 'on'
            
            # Processar fotos - upload para Supabase Storage (só se uma nova foto for enviada)
            if 'foto_principal' in request.FILES and request.FILES['foto_principal']:
                # Deletar foto antiga se existir
                if roupa.foto_principal_storage_path:
                    delete_image_from_supabase(roupa.foto_principal_storage_path)
                
                upload_result = upload_image_to_supabase(
                    request.FILES['foto_principal'], 
                    folder_name="roupas"
                )
                if upload_result['success']:
                    roupa.foto_principal = upload_result['public_url']
                    roupa.foto_principal_storage_path = upload_result['storage_path']
                else:
                    messages.error(request, f'Erro ao fazer upload da foto principal: {upload_result["error"]}')
                    return render(request, 'loja/admin/roupa_form.html', {'roupa': roupa, 'action': 'edit'})
            
            if 'foto_2' in request.FILES and request.FILES['foto_2']:
                # Deletar foto antiga se existir
                if roupa.foto_2_storage_path:
                    delete_image_from_supabase(roupa.foto_2_storage_path)
                
                upload_result = upload_image_to_supabase(
                    request.FILES['foto_2'], 
                    folder_name="roupas"
                )
                if upload_result['success']:
                    roupa.foto_2 = upload_result['public_url']
                    roupa.foto_2_storage_path = upload_result['storage_path']
                else:
                    messages.warning(request, f'Erro ao fazer upload da foto 2: {upload_result["error"]}')
            
            if 'foto_3' in request.FILES and request.FILES['foto_3']:
                # Deletar foto antiga se existir
                if roupa.foto_3_storage_path:
                    delete_image_from_supabase(roupa.foto_3_storage_path)
                
                upload_result = upload_image_to_supabase(
                    request.FILES['foto_3'], 
                    folder_name="roupas"
                )
                if upload_result['success']:
                    roupa.foto_3 = upload_result['public_url']
                    roupa.foto_3_storage_path = upload_result['storage_path']
                else:
                    messages.warning(request, f'Erro ao fazer upload da foto 3: {upload_result["error"]}')
            
            roupa.save()
            messages.success(request, f'Roupa "{roupa.nome}" atualizada com sucesso!')
            return redirect('admin_roupas_list')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar roupa: {str(e)}')
    
    return render(request, 'loja/admin/roupa_form.html', {'roupa': roupa, 'action': 'edit'})

@admin_required
@require_POST
def admin_roupa_delete(request, roupa_id):
    """Excluir roupa"""
    try:
        roupa = get_object_or_404(Roupa, id=roupa_id)
        nome_roupa = roupa.nome
        
        # Deletar imagens do Supabase Storage antes de deletar a roupa
        if roupa.foto_principal_storage_path:
            delete_image_from_supabase(roupa.foto_principal_storage_path)
        if roupa.foto_2_storage_path:
            delete_image_from_supabase(roupa.foto_2_storage_path)
        if roupa.foto_3_storage_path:
            delete_image_from_supabase(roupa.foto_3_storage_path)
        
        roupa.delete()
        messages.success(request, f'Roupa "{nome_roupa}" excluída com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir roupa: {str(e)}')
    
    return redirect('admin_roupas_list')

@admin_required
@require_POST
def admin_roupa_toggle_status(request, roupa_id):
    """Alternar status ativo/inativo da roupa"""
    try:
        roupa = get_object_or_404(Roupa, id=roupa_id)
        roupa.ativo = not roupa.ativo
        roupa.save()
        
        status = "ativada" if roupa.ativo else "desativada"
        messages.success(request, f'Roupa "{roupa.nome}" {status} com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao alterar status da roupa: {str(e)}')
    
    return redirect('admin_roupas_list')
