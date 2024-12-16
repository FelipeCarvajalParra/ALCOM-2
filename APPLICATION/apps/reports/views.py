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
from django.db.models.functions import TruncDate


@login_required
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def view_reports(request):
    # Parámetros de filtros
    date_range = request.GET.get('dateRange')
    selected_user = request.GET.get('user')
    selected_category = request.GET.get('category')

    # Rango de fechas: si no se selecciona, usar la última semana
    if date_range:
        start_date, end_date = date_range.split(" - ")
    else:
        end_date = now().date()
        start_date = end_date - timedelta(days=7)

    # Filtrar intervenciones
    filters = {'fecha_hora__date__range': [start_date, end_date]}
    if selected_user:
        try:
            user_id = CustomUser.objects.get(username=selected_user).id
            filters['usuario_fk'] = user_id
        except CustomUser.DoesNotExist:
            filters['usuario_fk'] = None  # Maneja el caso de un username inexistente

    if selected_category:
        filters['tarea_realizada'] = selected_category

    interventions = Intervenciones.objects.filter(**filters)

    # Agrupar por día (extraemos solo la fecha de fecha_hora) y por tipo (basado en tarea_realizada)
    grouped_data = (
        interventions
        .annotate(fecha=TruncDate('fecha_hora'))
        .values('fecha', 'tarea_realizada')
        .annotate(count=Count('num_orden_pk'))
        .order_by('fecha')
    )

    # Preparar datos para el gráfico
    categories = []
    data_by_type = {
        'intervenciones': [],
        'mantenimientos': [],
        'cambios de parte': []
    }

    for record in grouped_data:
        fecha = record['fecha']
        tarea = record['tarea_realizada']
        count = record['count']

        if fecha not in categories:
            categories.append(fecha)

        # Mapear las tareas a tipos conocidos
        if tarea == 'Intervenciones':  # Ajusta según los valores de tu modelo
            data_by_type['intervenciones'].append(count)
        elif tarea == 'Mantenimientos':
            data_by_type['mantenimientos'].append(count)
        elif tarea == 'Cambios de parte':
            data_by_type['cambios de parte'].append(count)

    # Asegurar que cada tipo tenga un dato por cada fecha
    for tipo, data in data_by_type.items():
        data_by_type[tipo] = [
            data[categories.index(fecha)] if fecha in categories else 0
            for fecha in categories
        ]

    # Retornar JSON si es una petición AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'categories': categories,
            'data': data_by_type
        })

    # Contexto para el template
    users_technicians = CustomUser.objects.filter(groups__name='technicians')
    context = {
        'usersTechnicians': users_technicians,
        'selectedUser': selected_user,
    }
    return render(request, "view_reports.html", context)
