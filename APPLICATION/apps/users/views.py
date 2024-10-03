from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.logIn.views import group_required
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from apps.logIn.models import CustomUser
from django.core.files.storage import default_storage
from django.core.paginator import Paginator


@login_required #Template para listar los usuarios
@group_required('administrators', redirect_url='expired_session')
def view_users(request):
    user_list = CustomUser.objects.all()  # Obtener todos los usuarios
    paginator = Paginator(user_list, 13)  # 15 usuarios por página

    page_number = request.GET.get('page')  
    users = paginator.get_page(page_number) 

    context = {
        'users': users,  # Pasar solo los usuarios de la página actual
    }
    return render(request, 'view_users.html', context)


@login_required #Template para listar los usuarios
@group_required('administrators', redirect_url='expired_session')
def edit_user(request, id):

    user = get_object_or_404(CustomUser, pk=id)

    context = {
        'user': user,  # Pasar solo los usuarios de la página actual
    }
    return render(request, 'user_edit.html', context)



























"""

@login_required #funcion que valida el usuario, se conecta con el archivo user validation.js
@group_required('administrators', redirect_url='expired_session')   
def validate_user(request):

    user = request.POST.get('user')

    if auth.objects.filter(username=user).exists():
        return JsonResponse({'error': 'El usuario ya existe'}, status=400)
    return JsonResponse({'success': True})

@login_required  #Template para agregar usuarios
@group_required('administrators', redirect_url='expired_session')
def admin_addUser(request):

    context = {
        'image_url': settings.MEDIA_URL + 'user_images/default_user.jpg'
    }

    return render(request, 'add_user-admin.html', context)


@login_required  #Template para agregar usuarios
@group_required('administrators', redirect_url='expired_session')
def register_user(request): #Funcionalidad para registrar a los nuevos usuarios
    if request.method == 'POST':
        try:
            username = request.POST.get('newUser-user')
            name = request.POST.get('newUser-name')
            job = request.POST.get('newUser-job')
            password = request.POST.get('newUser-password')
            picture = request.FILES.get('newUser-picture')

            # Crear el usuario
            user = auth(username=username, first_name=name, job=job)
            if password:
                user.set_password(password)  # Encriptar la contraseña
            if picture:
                user.picture = picture

            user.save()

            group_name = request.POST.get('newUser-role')
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            messages.success(request, '¡El usuario ha sido registrado satisfactoriamente!')
            return redirect('addUser')
        
        except Exception as e:
            messages.error(request, f'Ha ocurrido un error al registrar el usuario: {str(e)}')
            return redirect('addUser')

    messages.error(request, 'Método no permitido')
    return redirect('addUser')


@login_required  #Template para agregar usuarios
@group_required('administrators', redirect_url='expired_session')
def update_user_template(request, id):
    user = get_object_or_404(auth, pk=id)
    user_group = user.groups.first().name if user.groups.exists() else 'Sin Grupo'

    context = {
        'user': user,
        'user_group': user_group,
    }

    return render(request, 'update-user.html', context)

@login_required  #Template para agregar usuarios
@group_required('administrators', redirect_url='expired_session')
def update_user(request, id):
    usuario = get_object_or_404(auth, pk=id)

    
    usuario.first_name = request.POST.get('updateUser-name')
    usuario.job = request.POST.get('updateUser-job')
    usuario.username = request.POST.get('updateUser-user')

    if request.POST.get('updateUser-password'):
        usuario.set_password(request.POST.get('updateUser-password'))
    if request.FILES.get('updateUser-picture'): 
        if usuario.picture:# Si el usuario ya tiene una imagen, elimínala
            if default_storage.exists(usuario.picture.name):
                default_storage.delete(usuario.picture.name)
        usuario.picture = request.FILES.get('updateUser-picture')

    usuario.groups.clear()
    group = Group.objects.get(name=request.POST.get('updateUser-role'))
    usuario.groups.add(group)
    usuario.save()

    messages.success(request, 'Usuario actualizado correctamente')
    return redirect(f'/user/{id}/')

    """