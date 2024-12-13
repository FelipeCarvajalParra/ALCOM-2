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
from django.views.decorators.http import require_POST
from django.db import transaction


default_image = f"{settings.MEDIA_URL}default/default.jpg"


@login_required
@transaction.atomic
@group_required(['administrators', 'consultants', 'technicians'])
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
@transaction.atomic
@group_required(['administrators', 'consultants', 'technicians'], redirect_url='/forbidden_access/')
def site_construction(request):
    return render(request, 'construction.html')

def error_export(request):
    messages.error(request, 'Usted no tiene permiso para generar reportes.')
    return redirect('view_categories')

@login_required
@group_required(['administrators', 'consultants', 'technicians'], redirect_url='/forbidden_access/')
def search_general(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        search_query = request.GET.get('search_general', '').strip()  # Elimina espacios en blanco

        # Si el término de búsqueda está vacío, devolver una respuesta vacía
        if not search_query:
            empty_body = render_to_string('partials/_search_general_results.html', {
                'user_results': [],
                'category_results': [],
                'reference_results': [],
                'equipment_results': [],
                'default_image': default_image
            }, request=request)
            return JsonResponse({'body': empty_body})

        # Filtrar resultados con coincidencias parciales
        user_results = CustomUser.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
        category_results = Categorias.objects.filter(Q(nombre__icontains=search_query))
        reference_results = Referencias.objects.filter(referencia_pk__icontains=search_query).select_related('archivos')
        equipment_results = Equipos.objects.filter(
            Q(serial__icontains=search_query) | Q(cod_equipo_pk__icontains=search_query)
        )

        # Renderizar el partial con los resultados
        context = {
            'user_results': user_results,
            'category_results': category_results,
            'reference_results': reference_results,
            'equipment_results': equipment_results,
            'default_image': default_image
        }
        html_body = render_to_string('partials/_search_general_results.html', context, request=request)

        return JsonResponse({'body': html_body})

    # Si no es una solicitud AJAX, devuelve un error 400
    return JsonResponse({'error': 'Invalid request'}, status=400)
