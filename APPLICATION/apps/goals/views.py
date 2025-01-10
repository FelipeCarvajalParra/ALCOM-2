from django.http import JsonResponse
from .models import Metas
from apps.users.models import CustomUser
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from apps.logIn.views import group_required
from apps.inserts.models import Intervenciones

import datetime
from django.utils import timezone


def get_date_range_from_week(week_str):
    # Parsear la cadena de la semana "YYYY-Www" (ej. "2025-W02")
    year, week = week_str.split('-W')
    year = int(year)
    week = int(week)

    first_day_of_week = datetime.date(year, 1, 1) + datetime.timedelta(weeks=week-1)
    first_day_of_week = first_day_of_week - datetime.timedelta(days=first_day_of_week.weekday())  # Ajustar al lunes

    last_day_of_week = first_day_of_week + datetime.timedelta(days=6)

    # Convertir las fechas a formato dd/mm/yyyy
    start_date = first_day_of_week.strftime('%d/%m/%Y')
    end_date = last_day_of_week.strftime('%d/%m/%Y')

    return f'{start_date} - {end_date}'

from datetime import timedelta

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def new_goat(request):
    goalWeek = request.POST.get('goalWeek')
    goalCant = int(request.POST.get('goalCant'))
    user = request.POST.get('user')

    if goalWeek is None or goalCant is None or user is None:
        return JsonResponse({'error': 'Rellene todos los campos'})

    userObjet = get_object_or_404(CustomUser, pk=user)
    date_range = get_date_range_from_week(goalWeek)
    
    if Metas.objects.filter(rango_fechas=date_range, usuario_fk=userObjet).exists():
        return JsonResponse({'error': 'Ya existe una meta para este usuario en esta semana'})

    try:
        start_date_str, end_date_str = date_range.split(' - ')

        start_date = timezone.make_aware(
            datetime.datetime.strptime(start_date_str, '%d/%m/%Y').replace(hour=0, minute=0, second=0, microsecond=0),
            timezone.get_current_timezone()  # Usa la zona horaria actual configurada en Django
        )

        end_date = timezone.make_aware(
            datetime.datetime.strptime(end_date_str, '%d/%m/%Y').replace(hour=23, minute=59, second=59, microsecond=999999),
            timezone.get_current_timezone() 
        )
    except ValueError:
        return JsonResponse({'error': 'Ha ocurrido un error al procesar las fechas'})

    # Obtener la fecha actual
    current_date = timezone.now().date()

    # Calcular el primer día de la semana (lunes) y el último día de la semana (domingo) de la semana actual
    start_of_week = current_date - timedelta(days=current_date.weekday())  # Lunes
    end_of_week = start_of_week + timedelta(days=6)  # Domingo

    if start_date.date() < start_of_week:
        return JsonResponse({'error': 'La meta no puede ser añadida para una semana pasada.'})

    if start_date.date() >= start_of_week:
        interventions = Intervenciones.objects.filter(
            usuario_fk=userObjet,
            fecha_hora__range=[start_date, end_date],
            estado='Aprobada'
        ).count()

        # Crear la meta
        meta = Metas(
            meta=goalCant,
            rango_fechas=date_range,
            usuario_fk=userObjet,
            progreso=min(interventions, goalCant),  # Si el progreso no debe exceder la meta
            completado=interventions >= goalCant
        )
        meta.save()

        messages.success(request, 'Meta creada correctamente.')
        return JsonResponse({'success': True})


@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def delete_goal(request, id):
    try:
        id = int(id)  
        goal = get_object_or_404(Metas, meta_id=id)

        if goal.completado == 1:
            return JsonResponse({'error': 'No se puede eliminar una meta completada'}, status=400) 

        goal.delete() 
    except Http404:  
        return JsonResponse({'error': 'No se ha encontrado la meta'}, status=404)
    
    messages.success(request, 'Meta eliminada correctamente.')
    return JsonResponse({'success': True})