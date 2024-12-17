from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.logIn.views import group_required
from apps.users.models import CustomUser
from apps.inserts.models import Intervenciones
from django.http import JsonResponse
from django.template.loader import render_to_string
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
from django.utils import timezone


from django.utils import timezone

@login_required
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def view_reports2(request):
    # Obtener parámetros del filtro
    date_range = request.GET.get('dateRange')
    selected_user = request.GET.get('user')
    selected_category = request.GET.get('category')

    # Si no hay un rango de fechas, usar el mes actual por defecto
    if not date_range:
        today = datetime.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = today.replace(day=28) + timedelta(days=4)  # Garantiza que caiga en el último día del mes
        last_day_of_month = last_day_of_month - timedelta(days=last_day_of_month.day)
        date_range = f"{first_day_of_month.strftime('%Y-%m-%d')} - {last_day_of_month.strftime('%Y-%m-%d')}"

    # Procesar el rango de fechas
    start_date_str, end_date_str = date_range.split(" - ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Asegurar que las fechas sean conscientes de la zona horaria
    start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
    end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

    # Filtrar las intervenciones dentro del rango de fechas, usando fechas conscientes de la zona horaria
    interventions = Intervenciones.objects.filter(
        fecha_hora__range=[start_date, end_date]
    ).exclude(fecha_hora__isnull=True)  # Excluir registros con fecha nula

    print('start:', start_date, 'end:', end_date, 'interventions:', interventions)

    # Agrupar por fecha y tipo de tarea
    interventions_by_day = interventions.annotate(day=TruncDate('fecha_hora')).values('day', 'tarea_realizada').annotate(
        total=Count('num_orden_pk')
    ).order_by('day')

    print('inter:', interventions_by_day)

    # Crear un diccionario para estructurar los datos
    result = {
        'dates': [],
        'tasks': {
            'Intervencion': [],
            'Cambio de parte': [],
            'Mantenimiento': []
        }
    }

    # Llenar los datos
    for entry in interventions_by_day:
        if entry['day'] is not None:
            day = entry['day'].strftime("%Y-%m-%d")  # Formato de fecha para el gráfico
        else:
            continue  # Si 'day' es None, no lo añadimos

        # Añadir la fecha solo si no está ya en las categorías
        if day not in result['dates']:
            result['dates'].append(day)

        # Añadir el conteo a la tarea correspondiente
        task = entry['tarea_realizada']
        count = entry['total']
        if task in result['tasks']:
            result['tasks'][task].append(count)
        else:
            result['tasks'][task].append(0)

    # Generar las fechas completas en el rango, para asegurar que cada día esté presente en el gráfico
    all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    all_dates_str = [date.strftime("%Y-%m-%d") for date in all_dates]

    # Asegurarse de que todas las tareas tengan un valor por cada fecha, incluso si no tienen intervenciones ese día
    for task in result['tasks']:
        while len(result['tasks'][task]) < len(all_dates_str):
            result['tasks'][task].append(0)  # Rellenar con 0 donde no haya intervenciones

    # Si la petición es AJAX, devolvemos los datos en formato JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'interventionsByDay': result,
            'categories': all_dates_str,
            'series': [
                {'name': 'Intervencion', 'data': result['tasks']['Intervencion']},
                {'name': 'Cambio de parte', 'data': result['tasks']['Cambio de parte']},
                {'name': 'Mantenimiento', 'data': result['tasks']['Mantenimiento']},
            ]
        })

    # Si no es AJAX, renderizamos la plantilla
    users_technicians = CustomUser.objects.filter(groups__name='technicians')

    context = {
        'usersTechnicians': users_technicians,
        'selectedUser': selected_user,
        'dateRange': date_range,
        'selectedCategory': selected_category,
        'interventionsByDay': result,  # Enviar las intervenciones agrupadas por día
    }

    # Renderizar la plantilla con el contexto
    return render(request, "view_reports.html", context)




import json


@login_required
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def view_reports(request):
    # Obtener parámetros del filtro
    date_range = request.GET.get('dateRange')
    selected_user = request.GET.get('user')
    selected_category = request.GET.get('category')

    if not date_range:
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
    intervenciones_counts = [0] * (delta.days + 1)
    cambios_partes_counts = [0] * (delta.days + 1)
    mantenimientos_counts = [0] * (delta.days + 1)

    # Filtrar las intervenciones dentro del rango de fechas
    interventions = Intervenciones.objects.filter(
        fecha_hora__range=[start_date, end_date]
    ).exclude(fecha_hora__isnull=True)

    # Contar las intervenciones por día y tipo
    for intervention in interventions:
        day_index = (intervention.fecha_hora.date() - start_date.date()).days
        if intervention.tarea_realizada == "Intervencion":
            intervenciones_counts[day_index] += 1
        elif intervention.tarea_realizada == "Cambio de parte":
            cambios_partes_counts[day_index] += 1
        elif intervention.tarea_realizada == "Mantenimiento":
            mantenimientos_counts[day_index] += 1

    # Construir el array en el formato deseado
    report_data = {
        "categories": categories,
        "series": [
            {
                "name": "Intervenciones",
                "data": intervenciones_counts
            },
            {
                "name": "Cambio de partes",
                "data": cambios_partes_counts
            },
            {
                "name": "Mantenimiento",
                "data": mantenimientos_counts
            }
        ]
    }

    # Si se quiere devolver como un JSON directamente desde la vista (por ejemplo, para una petición AJAX):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(report_data)

    # Enviar el reporte al contexto de la plantilla
    users_technicians = CustomUser.objects.filter(groups__name='technicians')
    context = {
        'usersTechnicians': users_technicians,
        'selectedUser': selected_user,
        'selectedCategory': selected_category,
        'reportData': json.dumps(report_data)  # Convertir a JSON antes de pasarlo a la plantilla
    }

    # Renderizar la plantilla con el contexto
    return render(request, "view_reports.html", context)