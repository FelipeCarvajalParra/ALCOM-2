from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from apps.logIn.views import group_required
from django.contrib import messages
from apps.users.models import CustomUser
from apps.categories.models import Categorias
from apps.equipments.models import Equipos
from apps.references.models import Referencias
from django.db.models import Q
from django.conf import settings
from django.template.loader import render_to_string
from django.db import transaction
from apps.inserts.models import Intervenciones
from datetime import datetime, timedelta
import json
from django.http import JsonResponse
from django.utils import timezone
from apps.goals.models import Metas
from django.http import JsonResponse
from datetime import datetime, time

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
            if timezone.is_naive(fecha_hora):
                fecha_hora = timezone.make_aware(fecha_hora)
            
            day = fecha_hora.date().strftime('%Y-%m-%d')
            task = entry['tarea_realizada']
            if day in data_by_task and task in data_by_task[day]:
                data_by_task[day][task] += entry['count']  # Acumular las intervenciones
        else:
            print('Fecha no encontrada en la entrada:', entry)


    # Buacar meta para la semana actual
    week_range = f"{(datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%d/%m/%Y')} - {(datetime.now() - timedelta(days=datetime.now().weekday()) + timedelta(days=6)).strftime('%d/%m/%Y')}"
    percentage = 0
    if Metas.objects.filter(rango_fechas=week_range, usuario_fk=user).exists():
        user_goal = Metas.objects.get(rango_fechas=week_range, usuario_fk=user)
        goal = f'{user_goal.progreso}/{user_goal.meta}'

        if user_goal.meta > 0:
            percentage = int((user_goal.progreso / user_goal.meta) * 100)
        
    else:
        goal = '⏱️'

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
            'goal': goal,
            'percentage': percentage
        },
        'graph': {
            'series': graph_series,
            'categories': days_of_week,
        }
    }

    today = datetime.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=28) + timedelta(days=4)  # Garantiza que caiga en el último día del mes
    last_day_of_month = last_day_of_month - timedelta(days=last_day_of_month.day)
    date_range = f"{first_day_of_month.strftime('%Y-%m-%d')} - {last_day_of_month.strftime('%Y-%m-%d')}"

    start_date_str, end_date_str = date_range.split(" - ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Asegurar que las fechas sean conscientes de la zona horaria
    start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
    end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

    # Crear una lista de días en el rango de fechas
    delta = end_date - start_date
    categories = [(start_date + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(delta.days + 1)]

    # Inicializar contadores para cada tipo de intervención
    interventions_counts = [0] * (delta.days + 1)
    changes_parts_counts = [0] * (delta.days + 1)
    maintenance_counts = [0] * (delta.days + 1)

    # Asegúrate de que los rangos incluyan el inicio y el final del día
    start_datetime = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())
    end_datetime = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())

    interventions = Intervenciones.objects.filter(
        fecha_hora__range=[start_datetime, end_datetime],
        usuario_fk=user.id
    ).exclude(fecha_hora__isnull=True)


    # Contar las intervenciones por día y tipo
    for intervention in interventions:
        day_index = (intervention.fecha_hora.date() - start_date.date()).days
        if intervention.tarea_realizada == "Intervencion":
            interventions_counts[day_index] += 1
        elif intervention.tarea_realizada == "Cambio de parte":
            changes_parts_counts[day_index] += 1
        elif intervention.tarea_realizada == "Mantenimiento":
            maintenance_counts[day_index] += 1


    # Construir el array en el formato deseado
    report_data = {
        "categories": categories,
        "series": [
            {
                "name": "Intervenciones",
                "data": interventions_counts
            },
            {
                "name": "Cambio de partes",
                "data": changes_parts_counts
            },
            {
                "name": "Mantenimiento",
                "data": maintenance_counts
            }
        ]
    }

    # Pasar el JSON al contexto
    context = {
        'data_json': json.dumps(data),  # Serializar el JSON
        'data_grafic_line': json.dumps(report_data)  # Convertir a JSON antes de pasarlo a la plantilla
    }

    return render(request, 'home.html', context)

@login_required
@transaction.atomic
@group_required(['administrators', 'consultants', 'technicians'], redirect_url='/forbidden_access/')
def site_construction(request):
    return render(request, 'construction.html')

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
