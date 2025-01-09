from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Q
from apps.users.models import CustomUser
from apps.activityLog.utils import log_activity
from django.core.exceptions import PermissionDenied

#Funcion para limitar la navegacion por rol 
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def group_required(group_names, redirect_url='login'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Verificar si el usuario está autenticado y pertenece al grupo
            if request.user.is_authenticated:
                if request.user.groups.filter(name__in=group_names).exists():
                    return view_func(request, *args, **kwargs)
            # Si el usuario no cumple las condiciones, se redirige
            if redirect_url:
                # Verifica si la URL está bien formateada o si se requiere una vista específica
                if redirect_url == 'login':
                    return redirect('login')  # Si tienes una vista llamada 'login' en tus urls.py
                else:
                    return redirect(redirect_url)  # Redirige a la URL especificada en el parámetro
            else:
                raise PermissionDenied  # Si no se especifica redirección, devolver error 403
        return _wrapped_view
    return decorator

@require_POST
def login_validate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Validar que ambos campos están completos
    if not username or not password:
        return JsonResponse({'error': 'Ups! debes completar todos los campos'})

    user = CustomUser.objects.filter(username=username).first()  # Buscar el usuario

    if user is None:
        return JsonResponse({'error': 'Credenciales incorrectas'})

    if user.status == 'blocked':
        return JsonResponse({'error': 'Tu cuenta está bloqueada. Contacta al administrador.'})

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is None:
        user.login_attempts += 1
        user.save()
        

        if user.login_attempts >= 3:
            user.status = 'blocked'
            user.save()
            log_activity(
                user= user.id,                       
                action='LOCKOUT',                     
                description=f'La cuenta ha sido bloqueada por exceder el número de intentos de inicio de sesión.',  
                link = f'/edit_user/{user.id}',
                category='USER_PROFILE'          
            )
            return JsonResponse({'error': 'Tu cuenta está bloqueada. Contacta al administrador.'})

        return JsonResponse({'error': 'Credenciales incorrectas'})

    login(request, authenticated_user)
    log_activity(
        user=request.user.id,                       
        action='LOGIN',                   
        description=f'El usuario ingreso al sistema.',  
        link=f'/edit_user/{user.id}',
        category='USER_PROFILE'          
    )
    user.login_attempts = 0
    user.save()

    if request.user.groups.filter(name='administrators').exists():
        return JsonResponse({'success': True, 'redirect_url': '/home/'})
    elif request.user.groups.filter(name='consultants').exists():
        return JsonResponse({'success': True, 'redirect_url': '/view_all_references/'})

# Función para cerrar sesión 
def logout_user(request):
    logout(request)
    return redirect('/accounts/login/')
