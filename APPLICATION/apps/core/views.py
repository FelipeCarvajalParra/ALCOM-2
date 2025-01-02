from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from apps.logIn.views import group_required
from django.contrib import messages
from io import BytesIO
from apps.users.models import CustomUser
from apps.categories.models import Categorias
from apps.equipments.models import Equipos
from apps.references.models import Referencias
from django.db.models import Q
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.db import transaction
from apps.inserts.models import Intervenciones
from datetime import datetime, timedelta
import json
from django.http import JsonResponse
from django.utils import timezone

default_image = f"{settings.MEDIA_URL}default/default.jpg"

from collections import defaultdict
from datetime import datetime, timedelta
import json
from django.db.models import Count

@login_required
@transaction.atomic
@group_required(['administrators', 'consultants', 'technicians'], redirect_url='/forbidden_access/')
def home(request):
    user = request.user

    # Fecha actual o simulada
    now = datetime.now()

    # Calcular inicio y fin del mes actual
    start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = (start_month + timedelta(days=31)).replace(day=1)
    end_month = next_month - timedelta(seconds=1)

    # Calcular inicio y fin de la semana actual
    start_week = now - timedelta(days=now.weekday())
    start_week = start_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_week = start_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

    # Filtros para intervenciones
    user_interventions = Intervenciones.objects.filter(usuario_fk=user.id)
    month_interventions_count = user_interventions.filter(
        fecha_hora__range=(start_month, end_month)
    ).count()
    week_interventions_count = user_interventions.filter(
        fecha_hora__range=(start_week, end_week)
    ).count()

    # Total de intervenciones
    total_intervention = user_interventions.count()

    # Agrupar datos para la gráfica (por días de la semana actual y tareas realizadas)
    interventions_by_day = user_interventions.filter(
        fecha_hora__range=(start_week, end_week)
    ).values('fecha_hora', 'tarea_realizada').annotate(count=Count('num_orden_pk'))

    # Inicializar datos de la semana
    days_of_week = [(start_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    data_by_task = {day: {'Cambio de parte': 0, 'Intervencion': 0, 'Mantenimiento': 0} for day in days_of_week}

    # Llenar los datos con las intervenciones agrupadas
    for entry in interventions_by_day:
        # Asegurarse de que 'fecha_hora' sea consciente de la zona horaria
        if entry['fecha_hora']:
            fecha_hora = entry['fecha_hora']
            # Si es naive, conviértelo a aware
            if timezone.is_naive(fecha_hora):
                fecha_hora = timezone.make_aware(fecha_hora)
            
            day = fecha_hora.date().strftime('%Y-%m-%d')
            task = entry['tarea_realizada']
            if day in data_by_task and task in data_by_task[day]:
                data_by_task[day][task] += entry['count']  # Acumular las intervenciones
        else:
            print('Fecha no encontrada en la entrada:', entry)

    # Preparar datos para la gráfica
    graph_series = [
        {
            'name': 'Cambio de partes',
            'data': [data_by_task[day].get('Cambio de parte', 0) for day in days_of_week]
        },
        {
            'name': 'Intervenciones',
            'data': [data_by_task[day].get('Intervencion', 0) for day in days_of_week]
        },
        {
            'name': 'Mantenimientos',
            'data': [data_by_task[day].get('Mantenimiento', 0) for day in days_of_week]
        }
    ]

    # Construir el JSON
    data = {
        'metrics': {
            'total_intervention': total_intervention,
            'month_interventions_count': month_interventions_count,
            'week_interventions_count': week_interventions_count,
        },
        'graph': {
            'series': graph_series,
            'categories': days_of_week,
        }
    }

    # Pasar el JSON al contexto
    context = {
        'data_json': json.dumps(data),  # Serializar el JSON
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
        if request.user.groups.first().name == 'administrators':
            user_results = CustomUser.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))

        if request.user.groups.first().name == 'administrators' or request.user.groups.first().name == 'technicians':
            category_results = Categorias.objects.filter(Q(nombre__icontains=search_query))
            equipment_results = Equipos.objects.filter(
                Q(serial__icontains=search_query) | Q(cod_equipo_pk__icontains=search_query)
            )

        reference_results = Referencias.objects.filter(referencia_pk__icontains=search_query).select_related('archivos')
        
        # Renderizar el partial con los resultados
        context = {
            'user_results': user_results if 'user_results' in locals() else None,
            'category_results': category_results if 'category_results' in locals() else None,
            'reference_results': reference_results if 'reference_results' in locals() else None,
            'equipment_results': equipment_results if 'equipment_results' in locals() else None,
            'default_image': default_image
        }
        html_body = render_to_string('partials/_search_general_results.html', context, request=request)

        return JsonResponse({'body': html_body})

    # Si no es una solicitud AJAX, devuelve un error 400
    return JsonResponse({'error': 'Invalid request'}, status=400)
