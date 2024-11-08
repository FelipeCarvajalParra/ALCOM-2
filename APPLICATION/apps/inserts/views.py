from django.http import JsonResponse
from django.shortcuts import render
from apps.partsInventory.models import Inventario
from .models import Actualizaciones
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib import messages


@login_required
@require_POST
@transaction.atomic
def add_parts(request, part_id):
    try:
        # Obtener la pieza en el inventario por su ID
        part = Inventario.objects.get(num_parte_pk=part_id)
        
        # Obtener los datos del formulario
        action = request.POST.get('action')
        amount = request.POST.get('amount')
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
            tipo_movimiento='entrada' if action == 'Añadir' else 'salida',
            fuente=action,
            cantidad=amount,
            observaciones=note
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
        return JsonResponse({'error': f'Error inesperado: {e}'})

