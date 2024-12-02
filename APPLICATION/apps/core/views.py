from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from apps.logIn.views import group_required
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.contrib import messages
from io import BytesIO
from apps.users.models import CustomUser
from apps.categories.models import Categorias
from apps.equipments.models import Equipos
from apps.references.models import Referencias
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from django.template.loader import render_to_string

default_image = f"{settings.MEDIA_URL}default/default.jpg"

@login_required
def home(request):
    now = datetime.now()
    current_hour = now.hour

    if current_hour < 12:
        greeting = f'¡Buenos días {request.user.first_name}!'
    elif 12 <= current_hour < 18:
        greeting = f'¡Buenas tardes {request.user.first_name}¡'
    else:
        greeting = "¡Hola!"

    context = {
        'greeting': greeting
    }

    return render(request, 'home.html', context)



@login_required
def site_construction(request):
    return render(request, 'construction.html')



def error_export(request):
    messages.error(request, 'Usted no tiene permiso para generar reportes.')
    return redirect('view_categories')


def search_general(request):
    search_query = request.GET.get('search', '')

    # Filtrar resultados con coincidencias parciales
    user_results = CustomUser.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))

    category_results = Categorias.objects.filter(Q(nombre__icontains=search_query))

    reference_results = Referencias.objects.filter(referencia_pk__icontains=search_query).select_related('archivos')
    
    equipment_results = Equipos.objects.filter(
        Q(serial__icontains=search_query) | Q(cod_equipo_pk__icontains=search_query)
    )

    # Renderizar el partial con los resultados y devolver como JSON
    context = render_to_string('partials/search_results.html', {
        'user_results': user_results,
        'category_results': category_results,
        'reference_results': reference_results,
        'equipment_results': equipment_results,
        'default_image': default_image
    })


    return JsonResponse({'body': context})