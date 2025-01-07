from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.logIn.views import group_required
from apps.users.models import CustomUser
from apps.inserts.models import Intervenciones
from django.http import JsonResponse
from datetime import timedelta
from datetime import datetime, timedelta
from django.utils import timezone
import json
from datetime import datetime, time
from django.db.models import Q

@login_required
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def view_reports(request):
    # Obtener parámetros del filtro
    date_range = request.GET.get('dateRange')
    selected_user = request.GET.get('filterUser')
    selected_category = request.GET.get('filterCategory')

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
    interventions_counts = [0] * (delta.days + 1)
    changes_parts_counts = [0] * (delta.days + 1)
    maintenance_counts = [0] * (delta.days + 1)

    # Asegúrate de que los rangos incluyan el inicio y el final del día
    start_datetime = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())
    end_datetime = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())

    interventions = Intervenciones.objects.filter(
        fecha_hora__range=[start_datetime, end_datetime]
    ).exclude(fecha_hora__isnull=True)

    if selected_user and selected_user not in ["Usuario", "TODOS"]:
        reference_user = get_object_or_404(CustomUser, username=selected_user)
        interventions = interventions.filter(usuario_fk=reference_user.id)
    
    if selected_category and selected_category not in ["Procedimiento", "TODOS"]:
        interventions = interventions.filter(tarea_realizada=selected_category)

    # Contar las intervenciones por día y tipo
    for intervention in interventions:
        day_index = (intervention.fecha_hora.date() - start_date.date()).days
        if intervention.tarea_realizada == "Intervencion":
            interventions_counts[day_index] += 1
        elif intervention.tarea_realizada == "Cambio de parte":
            changes_parts_counts[day_index] += 1
        elif intervention.tarea_realizada == "Mantenimiento":
            maintenance_counts[day_index] += 1

    # Construir el mensaje de rango dinámico
    range_message = f"Rango: {date_range}"  # Mensaje base con el rango de fechas

    if selected_user and selected_user not in ["Usuario", "TODOS"]:
        reference_user = get_object_or_404(CustomUser, username=selected_user)
        range_message += f", Usuario: {reference_user.get_full_name()}"  # Agregar el nombre completo del usuario

    if selected_category and selected_category not in ["Procedimiento", "TODOS"]:
        range_message += f", Procedimiento: {selected_category}"  # Agregar el procedimiento seleccionado

    # Construir el array en el formato deseado
    report_data = {
        "range": range_message,  # Usar el mensaje dinámico
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

    # Si se quiere devolver como un JSON directamente desde la vista (por ejemplo, para una petición AJAX):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(report_data)

    users_technicians = CustomUser.objects.filter(Q(groups__name='technicians') | Q(groups__name='administrators'))
    context = {
        'usersTechnicians': users_technicians,
        'selectedUser': selected_user,
        'selectedCategory': selected_category,
        'reportData': json.dumps(report_data)  # Convertir a JSON antes de pasarlo a la plantilla
    }

    # Renderizar la plantilla con el contexto
    return render(request, "view_reports.html", context)
