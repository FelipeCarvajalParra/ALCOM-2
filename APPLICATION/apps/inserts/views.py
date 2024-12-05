from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.partsInventory.models import Inventario
from django.db.models import Max, Q
from .models import Actualizaciones, Intervenciones
from apps.users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib import messages
from django.utils import timezone
from django.template.loader import render_to_string
import json
from django.shortcuts import get_object_or_404
from apps.equipments.models import Equipos
from apps.activityLog.models import ActivityLog
from django.shortcuts import render
from django.urls import reverse
from apps.activityLog.utils import log_activity
from apps.logIn.views import group_required
from django.core.paginator import Paginator
from datetime import datetime, timedelta


@login_required
@require_POST
@transaction.atomic
def add_parts(request, part_id):
    try:
        # Obtener la pieza en el inventario por su ID
        part = Inventario.objects.get(num_parte_pk=part_id)
        action = request.POST.get('action')
        source = request.POST.get('source')

        amount = request.POST.get('amount')
        if int(amount) <= 0:
            return JsonResponse({'error': 'La cantidad ingresada no es válida.'})
        
        note = request.POST.get('note')

        # Validaciones de campo
        if not action or not amount:
            return JsonResponse({'error': 'Todos los campos son obligatorios.'})

        # Verificar si se ha seleccionado una acción válida
        if action == "Accion":
            return JsonResponse({'error': 'Por favor selecciona una acción válida: Añadir o Sustraer.'})

        # Convertir 'amount' a número y verificar que es válido
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'La cantidad ingresada no es válida.'})

        # Crear el registro en Actualizaciones
        updateStock = Actualizaciones.objects.create( 
            num_parte_fk=part,
            tipo_movimiento='Entrada' if action == 'Añadir' else 'Salida',
            fuente=source,
            cantidad=amount,
            observaciones=note, 
            fecha_hora=timezone.now()
        )

        # Verificar que se creó el registro en Actualizaciones antes de proceder
        if updateStock.pk:
            # Sumar o restar la cantidad en Inventario dependiendo de la acción
            if action == 'Añadir':
                part.total_unidades += amount
            elif action == 'Sustraer':
                if part.total_unidades < amount:
                    return JsonResponse({'error': 'No hay suficiente stock para sustraer esa cantidad.'})
                part.total_unidades -= amount
            part.save()  # Guardar los cambios en el inventario

            # Mensaje de éxito y respuesta
            messages.success(request, 'Stock actualizado correctamente.')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'No se pudo crear el registro en Actualizaciones'})

    except Inventario.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el registro en Inventario'})
    except Exception:
        return JsonResponse({'error': 'Error inesperado'})


@login_required
def consult_movements(request, movement_id):
    try:
        part = Actualizaciones.objects.get(actualizacion_pk=movement_id)

        if part.fecha_hora:
            part.fecha_hora = timezone.localtime(part.fecha_hora)
            part.fecha_hora = part.fecha_hora.strftime('%d/%m/%y - %I:%M %p')
        else:
            part.fecha_hora = None

        return JsonResponse({
            'movement': [
                {
                    'type_movement': 'Entrada' if part.tipo_movimiento == 'Entrada' else 'Salida',
                    'source': part.fuente,
                    'amount': part.cantidad,
                    'observations': part.observaciones if part.observaciones else 'Sin observaciones',
                    'date': part.fecha_hora
                }
            ]
        })
    
    except Inventario.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el registro en Inventario'})
    

from django.conf import settings

@login_required
@require_POST
@transaction.atomic
def consult_interventions(request, intervention_id):
    try:
        # Obtener la instancia de la intervención
        intervention = Intervenciones.objects.get(num_orden_pk=intervention_id)

        # Obtener el usuario asociado a la intervención
        user_intervention = intervention.usuario_fk
        es_admin = request.user.groups.filter(name='Administrators').exists()

        # Obtener ingresos y salidas
        parts_income = Actualizaciones.objects.filter(num_orden_fk=intervention.num_orden_pk, tipo_movimiento='Entrada')
        parts_outcome = Actualizaciones.objects.filter(num_orden_fk=intervention.num_orden_pk, tipo_movimiento='Salida')

        # Obtener la URL del PDF
        
        pdf_url = f"{settings.MEDIA_URL}{intervention.formato}" if intervention.formato else ""

    
        context = {
            'intervention': intervention,
            'user_intervention': user_intervention,
            'parts_income': parts_income,
            'parts_outcome': parts_outcome,
            'pdf_url': pdf_url,
            'es_admin': es_admin
        }

        # Renderizar el HTML del parcial
        html_body = render_to_string('partials/_interventions_containers.html', context, request=request)

        return JsonResponse({'body': html_body})

    except Intervenciones.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el registro en Intervenciones'})
    except Exception as e:
        return JsonResponse({'error': str(e)})


@login_required
def view_interventions(request):
    
    interventions = Intervenciones.objects.all().order_by('-fecha_hora')

    date_range = request.GET.get('dateRange')
    print(date_range)
    if date_range:
        try:
            start_date_str, end_date_str = date_range.split(' - ')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
            
            # Añade la zona horaria
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())
            
            # Filtrar por rango de fechas
            interventions = interventions.filter(fecha_hora__range=(start_date, end_date))
        except (ValueError, IndexError):
            pass

    search_query = request.GET.get('search', '').strip()
    if search_query:
        interventions = interventions.filter(
            Q(usuario_fk__first_name__icontains=search_query) |
            Q(usuario_fk__last_name__icontains=search_query)
        )

    paginator = Paginator(interventions, 15)
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page_number': page_number,
        'date_range': date_range,
        'search_query': search_query,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_all_interventions_table_body.html', context, request=request)
        html_footer = render_to_string('partials/_all_interventions_table_footer.html', context, request=request)
        return JsonResponse({'body': html_body, 'footer': html_footer})

    return render(request, 'view_interventions.html', context)


def num_orden(procedure):
    prefixes = {
        'Intervencion': 'INT',
        'Cambio de parte': 'CAM',
        'Mantenimiento': 'MAN'
    }

    # Obtener el prefijo correspondiente
    prefix = prefixes[procedure]
    
    # Filtrar registros por tipo de procedimiento y obtener el último valor numérico
    last_record = Intervenciones.objects.filter(tarea_realizada=procedure).aggregate(
        max_num=Max('num_orden_pk'))['max_num']

    if last_record:
        # Extraer el número eliminando el prefijo y convertirlo a entero
        last_number = int(last_record.replace(prefix, ''))
        next_number = last_number + 1
    else:
        # Si no hay registros previos, comenzar desde el primer número
        next_number = 1

    # Formatear el nuevo número con el prefijo y ceros iniciales
    return f"{prefix}{next_number:06d}"


@login_required
@require_POST
@transaction.atomic
def new_intervention(request):
    try:
        # Parsear los datos JSON
        data = json.loads(request.body)

        # Validar el procedimiento
        procedure = data.get('procedure', '').strip()
        if not procedure or procedure not in ['Intervencion', 'Cambio de parte', 'Mantenimiento']:
            return JsonResponse({'error': 'Por favor ingrese un procedimiento válido.'}, status=400)

        # Obtener intervenciones
        interventions = data.get('interventions', [])
        has_part_action = bool(interventions)

        # Validar intervenciones si existen
        for intervention in interventions:
            part_number = intervention.get('part')  # Número de parte
            amount = intervention.get('amount')  # Cantidad
            action = intervention.get('action', '').strip()  # Acción (Ingreso/Egreso)

            # Validación básica de intervención
            if not part_number or not amount or not action:
                return JsonResponse({'error': 'Cada movimiento debe tener número de parte, cantidad y acción.'}, status=400)
            if action not in ['Ingreso', 'Egreso']:
                return JsonResponse({'error': 'Por favor seleccione una acción válida.'}, status=400)

            # Validar existencia en inventario
            try:
                inventario_item = Inventario.objects.get(num_parte_pk=part_number)
            except Inventario.DoesNotExist:
                return JsonResponse({'error': f'El número de parte {part_number} no existe en el inventario.'}, status=404)

            # Validar cantidad disponible si es egreso
            if action == 'Ingreso' and int(amount) > inventario_item.total_unidades:
                return JsonResponse({'error': f'Cantidad insuficiente para la parte {part_number}.'}, status=400)

        # Validar observaciones generales si no hay intervenciones
        general_observations = data.get('generalObservations', '').strip()
        if not has_part_action and not general_observations:
            return JsonResponse({'error': 'Debe proporcionar una descripción general si no hay intervenciones.'}, status=400)

        # Validar equipo
        try:
            equipment_instance = Equipos.objects.get(cod_equipo_pk=data.get('codeEquipment').strip())
        except Equipos.DoesNotExist:
            return JsonResponse({'error': 'El equipo especificado no existe.'})

        intervention = Intervenciones.objects.create(
            num_orden_pk=num_orden(procedure),
            fecha_hora=timezone.now(),
            tarea_realizada=procedure,
            observaciones=general_observations,
            cod_equipo_fk=equipment_instance,
            usuario_fk=request.user,
            estado = 'Pendiente'
        )

        log_activity(
            user=request.user.id,                       
            action='CREATE',                 
            description=f'El usuario registro la intervencion {intervention.num_orden_pk}.',
            link=f'/edit_equipment/{equipment_instance.cod_equipo_pk}?intervention_id={intervention.num_orden_pk}',     
            category='INTERVENTIONS'          
        )

        # Procesar intervenciones específicas
        for update in interventions:
            part_instance = Inventario.objects.get(num_parte_pk=update.get('part').strip())  # Consulta segura porque ya se validó
            amount = int(update.get('amount'))  # Convertir a entero
            action = update.get('action', '').strip()
            observations = update.get('observations', '').strip()

            # Actualizar inventario
            if action == 'Ingreso':
                part_instance.total_unidades -= amount
            else:
                part_instance.total_unidades += amount
            part_instance.save()

            # Crear registro en Actualizaciones
            Actualizaciones.objects.create(
                num_orden_fk=intervention,
                num_parte_fk=part_instance,
                fuente=procedure,
                tipo_movimiento='Entrada' if action == 'Egreso' else 'Salida',
                observaciones=observations if observations else 'Sin observaciones',
                cantidad=amount,
            )

        # Responder con éxito
        return JsonResponse({'success': 'Datos procesados correctamente.'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al procesar los datos JSON.'})
    except Exception:
        return JsonResponse({'error': 'Error inesperado.'})



@login_required
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def order_service(request, num_order):

    # Obtener la intervención por su número de orden
    intervention = get_object_or_404(Intervenciones, num_orden_pk=num_order)
    equipment_instance = intervention.cod_equipo_fk
    intervention_income = Actualizaciones.objects.filter(num_orden_fk=intervention, tipo_movimiento='Salida')
    intervention_outcome = Actualizaciones.objects.filter(num_orden_fk=intervention, tipo_movimiento='Entrada')
    intervention_user =  get_object_or_404(CustomUser, pk = intervention.usuario_fk_id) 

    if intervention.estado != 'Pendiente':
        return redirect('edit_equipment', id_equipment=equipment_instance.cod_equipo_pk)
    
    
    context = {
        'equipment': equipment_instance,
        'intervention': intervention,
        'intervention_income': intervention_income,
        'intervention_outcome': intervention_outcome,
        'intervention_user': intervention_user
    }

    return render(request, 'orden_template.html', context)

import traceback

@login_required
@require_POST
@transaction.atomic
def save_result_intervention(request, num_order):
    try:
        # Verifica si la intervención existe
        intervention = get_object_or_404(Intervenciones, num_orden_pk=num_order)

        result = request.POST.get('result')
        uploaded_file = request.FILES.get('file', None)

        if result == 'passed':
            if uploaded_file:
                # Aquí estamos verificando que el archivo sea un PDF
                if uploaded_file.content_type == 'application/pdf':
                    intervention.formato = uploaded_file
                else:
                    return JsonResponse({'error': 'El archivo no es un PDF válido.'}, status=400)
            else:
                return JsonResponse({'error': 'No se ha recibido ningún archivo PDF.'}, status=400)

            intervention.estado = 'Aprobada'
            intervention.save()
            log_activity(
                user=request.user.id,                       
                action='CREATE',                 
                description=f'El usuario aprobo la intervencion {intervention.num_orden_pk}.',
                link=f'/edit_equipment/{intervention.cod_equipo_fk.cod_equipo_pk}?intervention_id={intervention.num_orden_pk}',     
                category='INTERVENTIONS'          
            )
            return JsonResponse({'message': 'La intervención ha sido aprobada correctamente.'})

        elif result == 'denied':

            registerLog = ActivityLog.objects.filter(link=f'/edit_equipment/{intervention.cod_equipo_fk.cod_equipo_pk}?intervention_id={intervention.num_orden_pk}')
            parts_income = Actualizaciones.objects.filter(num_orden_fk=intervention, tipo_movimiento='Entrada')
            parts_outcome = Actualizaciones.objects.filter(num_orden_fk=intervention, tipo_movimiento='Salida') 

            if parts_income:
                for part in parts_income:
                    part_rerefence = get_object_or_404(Inventario, num_parte_pk=part.num_parte_fk)
                    part_rerefence.total_unidades -= part.cantidad
                    part_rerefence.save()
                    part.delete()
            
            if parts_outcome:
                for part in parts_outcome:
                    part_rerefence = get_object_or_404(Inventario, num_parte_pk=part.num_parte_fk)
                    part_rerefence.total_unidades += part.cantidad
                    part_rerefence.save()
                    part.delete()

            equipment_intervention = intervention.cod_equipo_fk.cod_equipo_pk
            intervention.delete()
            registerLog.delete()
            
            return JsonResponse({'redirect_url': reverse('edit_equipment', kwargs={'id_equipment': equipment_intervention})})

        else:
            return JsonResponse({'error': 'Resultado no válido.'}, status=400)

    
    
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()  # Esto imprimirá el traceback completo del error
        return JsonResponse({'error': 'Error inesperado'})
    

    

    



