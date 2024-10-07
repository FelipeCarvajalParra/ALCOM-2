from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from .models import CustomUser
from apps.activityLog.models import ActivityLog


#Funcion para limitar la navegacion por rol 
def group_required(group_name, redirect_url='login'):
    def decorator(view_func):
        @user_passes_test(lambda u: u.groups.filter(name=group_name).exists(), login_url=redirect_url)
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Función para validar el rol del usuario 
@login_required
def redirect_user(request):
    if request.user.groups.filter(name='administrators').exists():
        return redirect('/home/construction')
    elif request.user.groups.filter(name='consultants').exists():
        return redirect('/home/construction')
    elif request.user.groups.filter(name='technicians').exists():
        return redirect('/home/construction')
    else:
        return redirect('GroupNone')
    
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
            return JsonResponse({'error': 'Tu cuenta está bloqueada. Contacta al administrador.'})

        return JsonResponse({'error': 'Credenciales incorrectas'})

    login(request, authenticated_user)
    log_activity(
                user=request.user.id,                       
                action='DELETE',                 
                title='Elimino usuario',      
                description=f'El usuario elimino el perfil de {user_instance.first_name}.',  
                category='USER_PROFILE'          
    )
    user.login_attempts = 0
    user.save()

    return JsonResponse({'success': True, 'redirect_url': '/redirect_user/'})

# Función para cerrar sesión 
def logout_user(request):
    logout(request)
    return redirect('/accounts/login/')
