from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.logIn.views import group_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from apps.logIn.models import CustomUser
from django.core.paginator import Paginator
import json

def get_group_by_name(group_name):
    """Obtiene un grupo por su nombre, o None si no existe."""
    try:
        return Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return None


@login_required
@group_required('administrators', redirect_url='expired_session')
def view_users(request):
    user_list = CustomUser.objects.all().order_by('-id')
    paginator = Paginator(user_list, 13)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    context = {'users': users}
    return render(request, 'view_users.html', context)


@login_required
@group_required('administrators', redirect_url='expired_session')
def edit_user(request, id):
    user = get_object_or_404(CustomUser, pk=id)
    context = {'user': user}
    return render(request, 'user_edit.html', context)


def validate_user_data(data, is_update=False):
    required_fields = ['names', 'lastName', 'email', 'jobName', 'username', 'status', 'group']

    if not is_update:
        required_fields.extend(['password', 'password_validation'])

    for field in required_fields:
        if not data.get(field):
            return {'success': False, 'error': f'El campo {field} es obligatorio.'}

    if not is_update and data['password'] != data['password_validation']:
        return {'success': False, 'error': 'Las contraseñas no coinciden.'}

    if CustomUser.objects.filter(username=data['username']).exists():
        return {'success': False, 'error': 'El usuario ya existe.'}

    if CustomUser.objects.filter(email=data['email']).exists():
        return {'success': False, 'error': 'El correo ya está registrado.'}

    group_mapping = {
        'Administrador': 'administrators',
        'Consultor': 'consultants',
        'Tecnico': 'technicians',
    }
    if group_mapping.get(data['group'], None) is None:
        return {'success': False, 'error': 'Grupo no válido.'}

    status_mapping = {
        'Activo': 'active',
        'Bloqueado': 'blocked',
    }
    if status_mapping.get(data['status'], None) is None:
        return {'success': False, 'error': 'Estado no válido.'}

    return {'success': True}


@login_required
@group_required('administrators', redirect_url='expired_session')
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        validation_result = validate_user_data(data)
        if not validation_result['success']:
            return JsonResponse(validation_result)

        try:
            group = get_group_by_name(data['group'])
            if not group:
                return JsonResponse({'success': False, 'error': 'Grupo no válido.'})

            new_user = CustomUser(
                username=data['username'],
                email=data['email'],
                first_name=data['names'].title(),
                last_name=data['lastName'].title(),
                position=data['jobName'],
                status=data['status'],
            )
            new_user.set_password(data['password'])
            new_user.save()
            new_user.groups.add(group)

            messages.success(request, 'Usuario registrado exitosamente.')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'Error al registrar el usuario: {str(e)}')
            return JsonResponse({'success': False, 'error': 'Error interno del servidor.'}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'})


@login_required
def update_personal_data(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        data = json.loads(request.body)
        errors = {}

        if 'names' in data and data['names'].strip():
            user.first_name = data['names'].strip().title()

        if 'lastName' in data and data['lastName'].strip():
            user.last_name = data['lastName'].strip().title()

        if 'email' in data and data['email'].strip():
            new_email = data['email'].strip().lower()
            if CustomUser.objects.filter(email=new_email).exclude(id=user.id).exists():
                return JsonResponse({'success': False, 'error': {'email': 'El correo ya está registrado por otro usuario.'}})

            user.email = new_email

        if 'jobName' in data and data['jobName'].strip():
            user.position = data['jobName'].strip()

        try:
            user.save()
            messages.success(request, 'Datos personales actualizados correctamente.')
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Error interno del servidor.'}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)


@login_required
@group_required('administrators', redirect_url='expired_session')
def update_login_data(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        data = json.loads(request.body)

        if 'username' in data and data['username'].strip():
            new_username = data['username'].strip()
            if CustomUser.objects.filter(username=new_username).exclude(id=user.id).exists():
                return JsonResponse({'success': False, 'error': 'El usuario ya existe.'})

            user.username = new_username

        if 'status' in data:
            user.status = 'active' if data['status'] == 'Activo' else 'blocked'

        if 'role' in data:
            group_name = {'Consultor': 'consultants', 'Administrador': 'administrators', 'Tecnico': 'technicians'}.get(data['role'])
            if group_name:
                user.groups.clear()
                group = get_group_by_name(group_name)
                if group:
                    user.groups.add(group)
                else:
                    return JsonResponse({'success': False, 'error': f'El grupo "{group_name}" no existe.'})

        if 'password' in data and data['password'].strip():
            if data['password'] == data.get('password_validation', ''):
                user.set_password(data['password'])
            else:
                return JsonResponse({'success': False, 'error': 'Las contraseñas no coinciden.'})

        user.save()
        messages.success(request, 'Datos de inicio de sesión actualizados correctamente.')
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)