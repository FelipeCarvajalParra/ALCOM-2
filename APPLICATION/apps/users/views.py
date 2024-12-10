from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.apps import apps
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from django.db import transaction
import json
import os
from apps.logIn.views import group_required
from apps.users.models import CustomUser
from apps.activityLog.models import ActivityLog
from apps.activityLog.utils import log_activity
from django.http import HttpResponseForbidden
from apps.inserts.models import Intervenciones

group_name = {
    'Consultor': 'consultants', 
    'Administrador': 'administrators', 
    'Tecnico': 'technicians'
}

status_mapping = {
    'Activo': 'active',
    'Bloqueado': 'blocked',
}

def get_group_by_name(group_name):
    try:
        return Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return None
    
@login_required
@group_required(['administrators'], redirect_url='/forbidden_access/')
def view_users(request):
    user_list = CustomUser.objects.exclude(id=request.user.id).order_by('-id')
    search_query = request.GET.get('search', '')

    if search_query:
        user_list = user_list.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))

    paginator = Paginator(user_list,15)  # Número de elementos por página
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    context = {
        'paginator': paginator
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_user_table_body.html', context, request=request)
        html_footer = render_to_string('partials/_user_table_footer.html', context, request=request)
        return JsonResponse({'body': html_body, 'footer': html_footer})

    return render(request, 'view_users.html', context)




















from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.timezone import make_aware, get_current_timezone
from datetime import datetime
from collections import defaultdict
import json


@login_required
@group_required(['administrators', 'consultants', 'technicians'], redirect_url='/forbidden_access/')
def edit_user(request, id):

    if int(request.user.id) != int(id):
        if not request.user.groups.filter(name='administrators').exists():
            return redirect('/forbidden_access/')
        
    user = get_object_or_404(CustomUser, pk=id)
    activity = ActivityLog.objects.filter(user_id=id).order_by('-timestamp')

    paginator = Paginator(activity, 15)  # Este es el objeto Paginator completo
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Este es el objeto Page para la página actual

    # Accedemos al número total de páginas desde el objeto Paginator
    is_last_page = page_obj.number == paginator.num_pages


    # Filtramos las intervenciones
    interventionsCant = Intervenciones.objects.filter(usuario_fk_id=id)

    years = set()
    for yearInterventions in interventionsCant:
        years.add(yearInterventions.fecha_hora.year)

    # Comprobación de permisos
    if int(request.user.id) != int(id):
        if not request.user.groups.filter(name='administrators').exists():
            return redirect('/forbidden_access/')

    selected_date = request.GET.get('date')  # Formato: 'dd/mm/yyyy'

    # Filtrar intervenciones por fecha específica
    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, '%d/%m/%Y').date()
            tz = get_current_timezone()
            start_of_day = make_aware(datetime.combine(selected_date_obj, datetime.min.time()), timezone=tz)
            end_of_day = make_aware(datetime.combine(selected_date_obj, datetime.max.time()), timezone=tz)

            selected_date_interventions = interventionsCant.filter(fecha_hora__range=(start_of_day, end_of_day))

        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
    else:
        selected_date_interventions = []

    # Generar datos para el mapa de calor
    interventions_data = defaultdict(int)
    for intervention in interventionsCant:
        date_key = intervention.fecha_hora.date()
        interventions_data[date_key] += 1

    interventions_json = [
        {"date": date.strftime('%Y-%m-%d'), "interventions": count}
        for date, count in interventions_data.items()
    ]

    if selected_date:
        print('dato: ', type(selected_date_obj))

    
    # Crear contexto
    user = get_object_or_404(CustomUser, pk=id)
    context = {
        'paginator': page_obj,  # Usamos Page aquí
        'page_number': page_number,
        'is_last_page': is_last_page,
        'user_account': user,
        'interventions_json': json.dumps(interventions_json),
        'interventions': selected_date_interventions,
        'years': years,
        'selected_date': selected_date_obj if selected_date else None,
    }

    # Respuesta parcial para AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_healt_map_interventions_list.html', context, request=request)
        return JsonResponse({'body': html_body})

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
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def register_user(request):
    data = json.loads(request.body)

    validation_result = validate_user_data(data)
    if not validation_result['success']:
        return JsonResponse(validation_result)

    try:
        group = get_group_by_name(group_name[data['group']])
        if not group:
            return JsonResponse({'success': False, 'error': 'Grupo no válido.'})

        new_user = CustomUser(
            username=data['username'],
            email=data['email'],
            first_name=data['names'].title(),
            last_name=data['lastName'].title(),
            position=data['jobName'],
            status=status_mapping[data['status']] ,
        )
        new_user.set_password(data['password'])
        new_user.save()
        new_user.groups.add(group)

        log_activity(
            user=request.user.id,                       
            action='CREATE',                 
            description=f'El usuario registro a {data["names"].title()} en el sistema.',  
            link=f'/edit_user/{new_user.id}',      
            category='USERS'          
        )
        
        messages.success(request, 'Usuario registrado exitosamente.')
        return JsonResponse({'success': True})
    except Exception:
        messages.error(request, f'Error al registrar el usuario')
        return JsonResponse({'success': False, 'error': 'Error interno del servidor.'}, status=500)

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def update_personal_data(request, user_id):
    userAccount = get_object_or_404(CustomUser, id=user_id)
    print('usuario', userAccount)
    data = json.loads(request.body)
    print('data', data)

    if not all([data.get('names', '').strip(), data.get('lastName', '').strip(), data.get('email', '').strip()]):
        return JsonResponse({'success': False, 'error': 'Todos los campos son requeridos.'}, status=400)

    if 'names' in data and data['names'].strip():
        userAccount.first_name = data['names'].strip().title()

    if 'lastName' in data and data['lastName'].strip():
        userAccount.last_name = data['lastName'].strip().title()

    if 'email' in data and data['email'].strip():
        new_email = data['email'].strip().lower()
        if new_email != userAccount.email:
            if CustomUser.objects.filter(email=new_email).exists():
                return JsonResponse({'success': False, 'error': {'email': 'El correo ya está registrado por otro usuario.'}})
            userAccount.email = new_email

    if 'jobName' in data and data['jobName'].strip():
        userAccount.position = data['jobName'].strip()

    log_action = (
        f'El usuario editó su informacion personal.' if userAccount.id == request.user.id
        else f'El usuario editó la informacion personal de {userAccount.username}.'
    )
    log_activity(
        user=request.user.id,
        action='UPDATE',
        description=log_action,
        link=f'/edit_user/{userAccount.id}' if userAccount.id != request.user.id else None,
        category='USER_PROFILE'
    )

    try:
        userAccount.save()
        messages.success(request, 'Datos personales actualizados correctamente.')
        return JsonResponse({'success': True})
    except Exception:
        return JsonResponse({'success': False, 'error': 'Error interno del servidor.'}, status=500)


@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
@group_required(['administrators', 'consultants', 'technicians'], redirect_url='/forbidden_access/')
def update_login_data(request, user_id):
    user_to_update = get_object_or_404(CustomUser, id=user_id)  # Usuario que será actualizado
    data = json.loads(request.body)

    # Variables de control
    role_changed = False
    changes = []

    # Validación y actualización de username
    if 'username' in data and data['username']:
        new_username = data['username'].strip()
        if CustomUser.objects.filter(username=new_username).exclude(id=user_to_update.id).exists():
            return JsonResponse({'success': False, 'error': 'El usuario ya existe.'})
        if user_to_update.username != new_username:
            user_to_update.username = new_username
            changes.append("username")
    else:
        return JsonResponse({'success': False, 'error': 'El usuario es obligatorio.'})

    # Validación y actualización de role
    if 'role' in data:
        group_name = {'Consultor': 'consultants', 'Administrador': 'administrators', 'Tecnico': 'technicians'}.get(data['role'])
        if group_name:
            user_to_update.groups.clear()
            group = get_group_by_name(group_name)
            if group:
                user_to_update.groups.add(group)
                role_changed = True
            else:
                return JsonResponse({'success': False, 'error': f'El grupo "{group_name}" no existe.'})

    # Validación y actualización de password
    if 'password' in data and data['password'].strip():
        if data['password'] == data.get('password_validation', ''):
            user_to_update.set_password(data['password'])
            changes.append("password")
        else:
            return JsonResponse({'success': False, 'error': 'Las contraseñas no coinciden.'})

    try:
        user_to_update.save()

        # Registro de actividad
        is_self_update = request.user.id == user_to_update.id

        # Actividad general
        log_activity(
            user=request.user.id,
            action='LOGIN',
            description=(
                'El usuario editó sus datos de inicio de sesión.'
                if is_self_update else
                f'El usuario actualizó los datos de inicio de sesión de {user_to_update.username}.'
            ),
            link=f'/edit_user/{user_to_update.id}' if not is_self_update else None,
            category='USER_PROFILE'
        )

        # Actividad específica si cambió el rol
        if role_changed:
            log_activity(
                user=request.user.id,
                action='LOGIN',
                description=(
                    f'El usuario cambió su rol a "{data["role"]}".'
                    if is_self_update else
                    f'El usuario cambió el rol de {user_to_update.username} a "{data["role"]}".'
                ),
                link=f'/edit_user/{user_to_update.id}' if not is_self_update else None,
                category='USER_PROFILE'
            )

        messages.success(request, 'Datos de inicio de sesión actualizados correctamente.')
        return JsonResponse({'success': True})

    except Exception:
        return JsonResponse({'success': False, 'error': 'Error interno del servidor.'}, status=500)

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def delete_user(request, user_id):
    try:
        user_instance = get_object_or_404(CustomUser, id=user_id)

        print(user_instance.id)

        # Verificar si la imagen no es la por defecto
        if user_instance.profile_picture and user_instance.profile_picture.url != settings.MEDIA_URL + 'default/default_user.jpg':
            # Obtener la ruta completa de la imagen
            image_path = user_instance.profile_picture.path
            # Eliminar la imagen del sistema de archivos
            if os.path.exists(image_path):
                os.remove(image_path)
        user_instance.delete()

        log_activity(
            user=request.user.id,                       
            action='DELETE',                 
            description=f'El usuario elimino el perfil de {user_instance.first_name}.',  
            category='USER_PROFILE'          
        )
        messages.success(request, 'Usuario eliminado correctamente.')
        return HttpResponse(status=200)  # Respuesta exitosa
    except Exception as e:
        messages.error(request, 'Ha ocurrido un error al eliminar el usuario.')
        return HttpResponse(status=500)  # Error interno en el servidor
