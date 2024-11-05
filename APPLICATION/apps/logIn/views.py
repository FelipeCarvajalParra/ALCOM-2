from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Q
from apps.users.models import CustomUser
from apps.activityLog.utils import log_activity

#Funcion para limitar la navegacion por rol 
def group_required(group_names, redirect_url='login'):
    def decorator(view_func):
        @user_passes_test(lambda u: u.groups.filter(Q(name__in=group_names)).exists(), login_url=redirect_url)
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
    
def expired_session(request): #Funcion que caduca la sesion por navegacion en url no permitida 
    logout(request)
    messages.error(request, 'Sesion caducada por navegacion sospechosa, evite ingresar a sitios no permitidos')
    return redirect('/accounts/login/')

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
            print(user.id)
            log_activity(
                user= user.id,                       
                action='LOCKOUT',                 
                title='Cuenta bloqueada.',      
                description=f'La cuenta del del usuario ha sido bloqueada por actividad sospechosa.',  
                link = f'/edit_user/{user.id}',
                category='USER_PROFILE'          
            )
            return JsonResponse({'error': 'Tu cuenta está bloqueada. Contacta al administrador.'})

        return JsonResponse({'error': 'Credenciales incorrectas'})

    login(request, authenticated_user)
    log_activity(
        user=request.user.id,                       
        action='LOGIN',                 
        title='Inicio de sesion',      
        description=f'El usuario ingreso al sistema.',  
        category='USER_PROFILE'          
    )
    user.login_attempts = 0
    user.save()

    return JsonResponse({'success': True, 'redirect_url': '/home/'})

# Función para cerrar sesión 
def logout_user(request):
    logout(request)
    return redirect('/accounts/login/')
