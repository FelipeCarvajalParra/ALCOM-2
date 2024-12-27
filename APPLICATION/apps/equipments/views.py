from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from apps.references.models import Referencias
from apps.categories.models import Categorias
from django.template.loader import render_to_string
from .models import Equipos
from apps.inserts.models import Intervenciones, Actualizaciones
from django.core.paginator import Paginator
import json
from apps.activityLog.utils import log_activity
from django.conf import settings
from apps.logIn.views import group_required
from django.utils import timezone


@login_required
@transaction.atomic
@group_required(['administrators', 'technicians'], redirect_url='/forbidden_access/')
def view_equipments(request):
    equipment_list = Equipos.objects.select_related('referencia_fk').all()
    categories_list = Categorias.objects.values_list('nombre', flat=True)
    brand_list = Referencias.objects.values_list('marca', flat=True).distinct()

    search_query = request.GET.get('search', '').strip()
    filter_brand = request.GET.get('brand', '').strip()
    filter_category = request.GET.get('category', '').strip()

    if search_query:
        equipment_list = equipment_list.filter(cod_equipo_pk__icontains=search_query)

    if filter_brand and filter_brand not in ['Marca', 'TODAS', '']:
        equipment_list = equipment_list.filter(referencia_fk__marca__icontains=filter_brand)
    
    if filter_category and filter_category not in ['Categoria', 'TODAS', '']:
        equipment_list = equipment_list.filter(referencia_fk__categoria__nombre__icontains=filter_category)

    paginator = Paginator(equipment_list, 15)
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'categories_list': categories_list,
        'brand_list': brand_list,
        'brand': filter_brand,
        'search_query': search_query,
        'category': filter_category
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_equipments_table_body.html', context, request=request)
        html_footer = render_to_string('partials/_equipments_table_footer.html', context, request=request)
        return JsonResponse({'body': html_body, 'footer': html_footer})

    return render(request, 'equipments.html', context)

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
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
            description=f'El usuario registró el equipo {new_reference.cod_equipo_pk}.',
            link=f'/edit_equipment/{new_reference.cod_equipo_pk}', 
            category='EQUIPMENTS'
        )
        messages.success(request, 'Existencia registrada correctamente')
        return JsonResponse({'success': True}, status=201)  # 201 Created

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al procesar los datos.'}, status=400)
    except Exception:
        return JsonResponse({'error':'Error inesperado'}) 
    

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def delete_equipment(request, id_equipment):
    try:
        # Obtener y eliminar la categoría
        equipment = get_object_or_404(Equipos, pk=id_equipment)
        equipmentCode = equipment.cod_equipo_pk
        equipment.delete()

        log_activity(
            user=request.user.id,
            action='DELETE',
            description=f'El usuario elimino el equipo {equipmentCode}.',
            category='EQUIPMENTS'
        )
        messages.success(request, 'Equipo eliminado correctamente.')
        return JsonResponse({'success': True}, status=200) 
    
    except Exception :
        messages.error(request, 'Ocurrió un error inesperado.')
        return JsonResponse({'success': True})  

@login_required
@transaction.atomic
@group_required(['administrators', 'technicians'], redirect_url='/forbidden_access/')
def edit_equipment(request, id_equipment):
    # Obtener el equipo y sus datos asociados
    equipment = get_object_or_404(Equipos, pk=id_equipment)
    reference = equipment.referencia_fk
    category = reference.categoria

    # Obtener todas las intervenciones para el equipo
    if request.user.groups.filter(name='Administrators').exists():
        interventions = Intervenciones.objects.filter(cod_equipo_fk=equipment).order_by('-fecha_hora')
    else:
        interventions = Intervenciones.objects.filter(cod_equipo_fk=equipment, usuario_fk=request.user).order_by('-fecha_hora')

    paginator_interventions = Paginator(interventions, 7)
    page_number_interventions = request.GET.get('page_interventions')
    paginator_interventions = paginator_interventions.get_page(page_number_interventions)

    # Obtener el parámetro de la intervención seleccionada (si existe)
    selected_intervention_id = request.GET.get('intervention_id')
    selected_intervention = None
    intervention_context = {} 

    if selected_intervention_id:
        try:
            selected_intervention = Intervenciones.objects.get(num_orden_pk=selected_intervention_id)

            user_intervention = selected_intervention.usuario_fk
            es_admin = request.user.groups.filter(name='Administrators').exists()
            parts_income = Actualizaciones.objects.filter(num_orden_fk=selected_intervention.num_orden_pk, tipo_movimiento='Entrada')
            parts_outcome = Actualizaciones.objects.filter(num_orden_fk=selected_intervention.num_orden_pk, tipo_movimiento='Salida')
            pdf_url = f"{settings.MEDIA_URL}{selected_intervention.formato}" if selected_intervention.formato else ""

            intervention_context = {
                'intervention': selected_intervention,
                'user_intervention': user_intervention,
                'parts_income': parts_income,
                'parts_outcome': parts_outcome,
                'pdf_url': pdf_url,
                'es_admin': es_admin,
            }
        except Intervenciones.DoesNotExist:
            selected_intervention = None

    # Si no se seleccionó ninguna intervención, se toma la más reciente
    if not selected_intervention:
        if interventions.exists():
            selected_intervention = interventions.first()

            user_intervention = selected_intervention.usuario_fk
            es_admin = request.user.groups.filter(name='Administrators').exists()
            parts_income = Actualizaciones.objects.filter(num_orden_fk=selected_intervention.num_orden_pk, tipo_movimiento='Entrada')
            parts_outcome = Actualizaciones.objects.filter(num_orden_fk=selected_intervention.num_orden_pk, tipo_movimiento='Salida')
            pdf_url = f"{settings.MEDIA_URL}{selected_intervention.formato}" if selected_intervention.formato else ""

            intervention_context = {
                'intervention': selected_intervention,
                'user_intervention': user_intervention,
                'parts_income': parts_income,
                'parts_outcome': parts_outcome,
                'pdf_url': pdf_url,
                'es_admin': es_admin
            }

    num_orden_pks = interventions.values_list('num_orden_pk', flat=True)

    if request.user.groups.filter(name='Administrators').exists():
        updates = Actualizaciones.objects.filter(num_orden_fk__in=num_orden_pks).order_by('-fecha_hora')
    else:
        updates = Actualizaciones.objects.filter(num_orden_fk__in=num_orden_pks, num_orden_fk__usuario_fk=request.user).order_by('-fecha_hora')

    # Paginación de actualizaciones
    paginator = Paginator(updates, 15)
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    # Contexto general para renderizar la plantilla
    context = {
        'equipment': equipment,
        'reference': reference,
        'category_equipment': category, 
        'interventions': paginator_interventions, 
        'selected_intervention': selected_intervention,  
        'paginator': paginator,  
        'page_number': page_number,  
        'page_number_interventions': page_number_interventions, 
        **intervention_context,
        'now': timezone.now()
    }

    return render(request, 'equipment_edit.html', context)


@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def edit_equipment_state(request):
    try:

        equipment_id = request.POST.get('codeEquipment')
        if not Equipos.objects.filter(pk=equipment_id).exists():
            return JsonResponse({'error': 'Equipo no encontrado.'})

        equipment = get_object_or_404(Equipos, pk=equipment_id)

        new_state = request.POST.get('state')
        if new_state not in ['Disponible', 'Revisar', 'Reparar']:
            return JsonResponse({'error': 'Estado inválido.'})

        equipment.estado = new_state
        equipment.save()

        log_activity(
            user=request.user.id,
            action='UPDATE',
            description=f'El usuario actualizó el estado del equipo {equipment.cod_equipo_pk}.',
            link=f'/edit_equipment/{equipment.cod_equipo_pk}', 
            category='EQUIPMENTS'
        )
        messages.success(request, 'Estado actualizado correctamente.')
        return JsonResponse({'success': True}, status=200)
    except Exception as e:
        return JsonResponse({'error': 'Ocurrio un error inesperado.'})
