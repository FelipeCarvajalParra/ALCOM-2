from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib import messages
from apps.partsInventory.models import Inventario
from apps.inserts.models import Actualizaciones
from .models import Compras
from apps.logIn.views import group_required
from apps.activityLog.utils import log_activity
from datetime import datetime
from django.utils.timezone import localtime

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def new_shopping(request):
    partid = request.POST.get('partId')
    color = request.POST.get('color')
    amount = request.POST.get('amountShopping')
    observations = request.POST.get('noteShopping')

    if not partid or not amount:
        return JsonResponse({'error': 'Complete los campos obligatorios.'})

    try:
        amount = int(amount)
        if amount < 1:
            return JsonResponse({'error': 'La cantidad debe ser mayor a 0.'})
    except ValueError:
        return JsonResponse({'error': 'La cantidad debe ser un número válido.'})

    partid = get_object_or_404(Inventario, pk=partid)

    try:
        new_shopping = Compras.objects.create(
            num_parte_fk=partid,
            cantidad=amount,
            color = color.capitalize(),
            observaciones= observations.capitalize()
        )

        log_activity(
            user=request.user.id,                       
            action='CREATE',                 
            description=f'El usuario registro un reporte de compra para la parte: {new_shopping.num_parte_fk.nombre}.',  
            link=f'/edit_part/{new_shopping.num_parte_fk.num_parte_pk}',      
            category='PARTS'          
        )
    except Exception:
        return JsonResponse({'error': 'Error inesperado al registrar la compra.'}, status=500)

    messages.success(request, 'Reporte de compra registrado correctamente')
    return JsonResponse({'success': True}, status=200)

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def delete_shopping(request, shopping_id):
    try:
        shopping = get_object_or_404(Compras, pk=shopping_id)
        part = get_object_or_404(Inventario, pk=shopping.num_parte_fk.num_parte_pk)   
        shopping.delete()

        log_activity(
            user=request.user.id,                       
            action='DELETE',                 
            description=f'El usuario elimino un reporte de compra para la parte: {part.nombre}.',  
            link=f'/edit_part/{part.num_parte_pk}',      
            category='PARTS'          
        )

        messages.success(request, 'Reporte de compra eliminado correctamente')
        return JsonResponse({'success': True})

    except Exception:
        messages.error(request, 'Ocurrió un error inesperado.')
        return JsonResponse({'success': True})
    

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def validate_shopping(request, shopping_id):
    try:
        shopping = get_object_or_404(Compras, pk=shopping_id)
        part = get_object_or_404(Inventario, pk=shopping.num_parte_fk.num_parte_pk)   
        
        new_movement = Actualizaciones.objects.create(
            num_parte_fk=part,
            cantidad=shopping.cantidad,
            tipo_movimiento='Entrada',
            fuente = 'Compra',
            fecha_hora = datetime.now(),
        )

        part.total_unidades += shopping.cantidad
        part.save()

        shopping.delete()

        log_activity(
            user=request.user.id,                       
            action='UPDATE',                 
            description=f'El usuario valido un reporte de compra para la parte: {part.nombre}.',  
            link=f'/edit_part/{part.num_parte_pk}',      
            category='PARTS'          
        )

        messages.success(request, 'Reporte de compra validado correctamente')
        return JsonResponse({'success': True})

    except Exception as e:
        print(e)
        messages.error(request, 'Ocurrió un error inesperado.')
        return JsonResponse({'success': True})

@login_required
@transaction.atomic
@group_required(['administrators', 'technicians'], redirect_url='/forbidden_access/')
def consult_shopping(request, shopping_id):
    try:
        shopping = get_object_or_404(Compras, pk=shopping_id)

        date = shopping.fecha_hora
        formatted_date = localtime(date).strftime('%d/%m/%Y - %I:%M%p') if date else None

        return JsonResponse({
            'shopping': {
                'partName': shopping.num_parte_fk.nombre,
                'partNumber': shopping.num_parte_fk.num_parte_pk,
                'amount': shopping.cantidad,
                'color': shopping.color,
                'date': formatted_date,
                'observations': shopping.observaciones
            }
        })
    except Exception:
        return JsonResponse({'error':'Error inesperado'}) 




