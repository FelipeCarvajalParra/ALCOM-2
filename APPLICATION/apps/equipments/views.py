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


@login_required
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
    
    if filter_category and filter_category not in ['Categoría', 'TODAS', '']:
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


@login_required
def edit_equipment(request, id_equipment):

    equipment = get_object_or_404(Equipos, pk=id_equipment)
    reference = equipment.referencia_fk
    category = reference.categoria
    interventions = Intervenciones.objects.filter(cod_equipo_fk=equipment).order_by('-fecha_hora')

    num_orden_pks = interventions.values_list('num_orden_pk', flat=True)
    updates = Actualizaciones.objects.filter(num_orden_fk__in=num_orden_pks).order_by('-fecha_hora')

    paginator_interventions = Paginator(interventions, 2)
    page_number_interventions = request.GET.get('page_interventions')
    paginator_interventions = paginator_interventions.get_page(page_number_interventions)

    paginator = Paginator(updates, 1)
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    context = {
        'equipment': equipment,
        'reference': reference,
        'category_equipment': category,  # Pasamos la categoría al contexto
        'interventions': paginator_interventions, 
        'paginator': paginator,
        'page_number': page_number,
        'page_number_interventions': page_number_interventions
    }

    return render(request, 'equipment_edit.html', context)
