from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from apps.references.models import Referencias
from .models import Equipos
import json
from apps.activityLog.utils import log_activity



@login_required
@require_POST
@transaction.atomic
def new_equipment(request):
    try:
        reference = request.POST.get('reference')
        code = request.POST.get('code')
        serial = request.POST.get('serial')
        state = request.POST.get('state')


        if Equipos.objects.filter(cod_equipo_pk=code).exists():
            return JsonResponse({'error': 'El codigo de equipo ya esta registrado.'}, status=400)

        if Equipos.objects.filter(serial=serial).exists():
            return JsonResponse({'error': 'El serial ya esta registrado.'}, status=400)
        
        if Referencias.objects.filter(referencia_pk=reference).exists():
            reference = get_object_or_404(Referencias, pk=reference)
        else:
            return JsonResponse({'error': 'Referencia invalida.'}, status=400)
        

        new_reference = Equipos.objects.create(
            referencia_fk = reference,
            cod_equipo_pk=code,
            serial=serial,
            estado= state,
        )

        
        log_activity(
            user=request.user.id,                       
            action='CREATE',                 
            title='Registro de equipo',      
            description=f'El usuario registró el equipo {code}',  
            link=f'/view_categories/view_references/',      
            category='CATEGORY'          
        )
        messages.success(request, 'Existencia registrada correctamente')
        return JsonResponse({'success': True}, status=201)  # 201 Created

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al procesar los datos.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@login_required
@require_POST
@transaction.atomic
def delete_equipment(request, id_equipment):
    try:
        # Obtener y eliminar la categoría
        equipment = get_object_or_404(Equipos, pk=id_equipment)
        equipment.delete()

        log_activity(
            user=request.user.id,                       
            action='DELETE',                 
            title='Elimino equipo',      
            description=f'El usuario elimino el equipo {equipment.cod_equipo_pk}.',  
            category='EQUIPMENT'          
        )
        messages.success(request, 'Equipo eliminado correctamente.')
        return JsonResponse({'success': True}, status=200) 
    
    except Exception as e:
        messages.error(request, 'Ocurrió un error inesperado.')
        return JsonResponse({'success': True})  