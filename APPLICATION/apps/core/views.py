from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime

@login_required
def home(request):
    # Obtener la hora actual
    now = datetime.now()
    current_hour = now.hour

    # Definir los saludos
    if current_hour < 12:
        greeting = f'¡Buenos días! {request.user.first_name}'
    elif 12 <= current_hour < 18:
        greeting = f'¡Buenas tardes! {request.user.first_name}'
    else:
        greeting = "¡Hola!"


    # Pasar los datos a la plantilla
    context = {
        'greeting': greeting
    }

    return render(request, 'home.html', context)


@login_required
def site_construction(request):
    return render(request, 'construction.html')

