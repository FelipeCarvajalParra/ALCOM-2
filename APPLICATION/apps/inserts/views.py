from django.http import JsonResponse
from django.shortcuts import render
from apps.partsInventory.models import Inventario
from .models import Actualizaciones, Intervenciones
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib import messages
from django.utils import timezone


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
    except Exception as e:
        print(e)
        return JsonResponse({'error': f'Error inesperado'})


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
