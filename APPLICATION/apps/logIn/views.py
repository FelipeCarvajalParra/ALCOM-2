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
        return redirect('admin_home')
    elif request.user.groups.filter(name='consultants').exists():
        return redirect('consultants_home')
    elif request.user.groups.filter(name='technicians').exists():
        return redirect('technicians_home')
    else:
        return redirect('GroupNone')
    
def expired_session(request): #Funcion que caduca la sesion por navegacion en url no permitida 
    logout(request)
    messages.error(request, 'Sesion caducada por navegacion sospechosa, evite ingresar a sitios no permitidos')
    return redirect('/accounts/login/')

def login_validate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Ups! debes completar todos los campos'}, status=400)

    # Buscar el usuario en la base de datos
    user = CustomUser.objects.filter(username=username).first()
    
    if user is None:
        return JsonResponse({'error': 'Credenciales incorrectas'}, status=400)

    if user.status == 'blocked':
        return JsonResponse({'error': 'Tu cuenta está bloqueada. Contacta al administrador.'}, status=403)

    # Autenticar al usuario
    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is None:
        # Aumentar el contador de intentos fallidos
        user.login_attempts += 1
        user.save()

        if user.login_attempts >= 3:
            user.status = 'blocked'
            user.save()
            return JsonResponse({'error': 'Tu cuenta está bloqueada. Contacta al administrador.'}, status=403)
        
        return JsonResponse({'error': 'Credenciales incorrectas'}, status=400)

    # Si las credenciales son correctas
    login(request, authenticated_user)

    # Reiniciar contador de intentos fallidos
    user.login_attempts = 0
    user.save()

    return JsonResponse({'success': True, 'redirect_url': '/redirect_user/'})











# Función para cerrar sesión 
def logout_user(request):
    logout(request)
    return redirect('/accounts/login/')
