from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from apps.shopping.models import Compras
from .models import Inventario
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Q
from apps.inserts.models import Actualizaciones
from django.db.models import Sum
from apps.logIn.views import group_required
from apps.activityLog.utils import log_activity
from apps.partsInventory.models import PiezasReferencias, Referencias

default_image = f"{settings.MEDIA_URL}default/default.jpg"

@login_required
@transaction.atomic
@group_required(['administrators', 'technicians'], redirect_url='/forbidden_access/')
def view_inventory_parts(request):

    part_list = Inventario.objects.all()
    search_query = request.GET.get('search', '').strip()

    if search_query:
        part_list = part_list.filter(
            Q(num_parte_pk__icontains=search_query) | Q(nombre__icontains=search_query)
        )

    paginator = Paginator(part_list, 15)
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'default_image': default_image
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_parts_table_body.html', context, request=request)
        html_footer = render_to_string('partials/_parts_table_footer.html', context, request=request)
        return JsonResponse({'body': html_body, 'footer': html_footer})

    return render(request, 'view_parts.html', context)

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def new_part(request):
    partNumber = request.POST.get('partNumber')
    namePart = request.POST.get('namePart')
    location = request.POST.get('location')

    if not partNumber or not namePart or not location:
        return JsonResponse({'error': 'Todos los campos son obligatorios.'})

    if Inventario.objects.filter(pk=partNumber).exists():
        return JsonResponse({'error': 'El número de parte ya existe.'})

    try:
        new_part = Inventario.objects.create(
            num_parte_pk=partNumber,
            nombre=namePart,
            ubicacion=location,
        )

        log_activity(
            user=request.user.id,                       
            action='CREATE',                 
            description=f'El usuario registro la parte: {new_part.nombre}.',  
            link=f'/edit_part/{new_part.num_parte_pk}',      
            category='PARTS'          
        )

    except Exception:
        return JsonResponse({'error': 'Error inesperado'})

    messages.success(request, 'Pieza registrada correctamente')
    return JsonResponse({'success': True})

@login_required
@transaction.atomic
@group_required(['administrators', 'technicians'], redirect_url='/forbidden_access/')
def edit_part(request, part_id):

    search = request.GET.get('search', '').strip()

    part = get_object_or_404(Inventario, pk=part_id)
    part_movements = Actualizaciones.objects.filter(num_parte_fk=part_id).order_by('-actualizacion_pk')

    shoppings = Compras.objects.filter(num_parte_fk=part_id).order_by('-fecha_hora')

    partsIncome = Actualizaciones.objects.filter(tipo_movimiento='Entrada', num_parte_fk=part_id).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    partsOutcome = Actualizaciones.objects.filter(tipo_movimiento='Salida', num_parte_fk=part_id).aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    search_mapping = {
        'Entradas': 'Entrada',
        'Salidas': 'Salida'
    }
    
    if search:
        search = search_mapping.get(search, search)
        part_movements = part_movements.filter(tipo_movimiento=search)

    paginator = Paginator(part_movements,11) 
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    paginator_shopping = Paginator(shoppings, 1)
    page_number_shopping = request.GET.get('page_shopping')
    paginator_shopping = paginator_shopping.get_page(page_number_shopping)

    references_associated = PiezasReferencias.objects.filter(num_parte_fk=part_id)
    paginator_references = Paginator(references_associated, 1)
    page_number_references = request.GET.get('page_references')
    paginator_references = paginator_references.get_page(page_number_references)

    context = {
        'paginator': paginator,
        'page_number': page_number,
        'search_query': search,
        'part': part,
        'default_image': default_image,
        'partsIncome': partsIncome,
        'partsOutcome': partsOutcome,
        'paginator_shopping': paginator_shopping,
        'page_number_shopping': page_number_shopping,
        'paginator_references': paginator_references,
        'page_number_references': page_number_references
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_movements_table_body.html', context, request=request)
        html_footer = render_to_string('partials/_movements_table_footer.html', context, request=request)
        return JsonResponse({'body': html_body, 'footer': html_footer})

    return render(request, 'edit_part.html', context)

@login_required
@transaction.atomic
@group_required(['administrators', 'technicians'], redirect_url='/forbidden_access/')
def consult_part(request, part_id):
    try:
        part = Inventario.objects.get(num_parte_pk=part_id)

        # Extraer la URL del archivo si existe
        manual_url = part.manual.url if part.manual else None
        description_part = (f"{part.nombre}>{part.num_parte_pk} ")

        return JsonResponse({
            'part': {
                'name': part.nombre,
                'number': part.num_parte_pk,
                'location': part.ubicacion,
                'stock': part.total_unidades,
                'url': part.link_consulta,
                'manual': manual_url,  # Enviar la URL del archivo o None si no existe
                'description_part': description_part
            }
        })
    except Inventario.DoesNotExist:
        return JsonResponse({'error': 'Part not found'})
    except Exception:
        return JsonResponse({'error':'Error inesperado'}) 
    
@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def edit_part_action(request, part_id):
    try:
        part = Inventario.objects.get(num_parte_pk=part_id)
        namePart = request.POST.get('namePart')
        location = request.POST.get('location')
        url = request.POST.get('url')
        linkShop1 = request.POST.get('linkShopping1')
        linkShop2 = request.POST.get('linkShopping2')
        linkShop3 = request.POST.get('linkShopping3')

        part.nombre = namePart
        part.ubicacion = location
        part.link_consulta = url
        part.link_compra_1 = linkShop1
        part.link_compra_2 = linkShop2
        part.link_compra_3 = linkShop3
        part.save()

        log_activity(
            user=request.user.id,                       
            action='UPDATE',                 
            description=f'El usuario edito la parte: {part.nombre}.',  
            link=f'/edit_part/{part.num_parte_pk}',      
            category='PARTS'          
        )
  
        messages.success(request, 'Pieza actualizada correctamente.')
        return JsonResponse({'succes': True})

    except Inventario.DoesNotExist:
        return JsonResponse({'error':'No se encontro el registro'})
    except Exception as e:
        return JsonResponse({'error':'Error inesperado'})

@login_required
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def view_movements(request):

    type_movement = request.GET.get('search', '').strip()
    movements = Actualizaciones.objects.all().order_by('-actualizacion_pk')

    if type_movement:
        if type_movement == 'Entradas':
            movements = Actualizaciones.objects.filter(tipo_movimiento='Entrada').order_by('-actualizacion_pk')
        elif type_movement == 'Salidas':
            movements = Actualizaciones.objects.filter(tipo_movimiento='Salida').order_by('-actualizacion_pk')

    paginator = Paginator(movements, 15)
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'search_query': type_movement,
        'page_number': page_number
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_movements_table_body.html', context, request=request)
        html_footer = render_to_string('partials/_movements_table_footer.html', context, request=request)
        return JsonResponse({'body': html_body, 'footer': html_footer})

    return render(request, 'view_movements.html', context)

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def delete_part_reference(request, partReference_id):
    try:
        # Obtener y eliminar la categoría
        part_reference = get_object_or_404(PiezasReferencias, pk=partReference_id)

        part = part_reference.num_parte_fk
        reference = part_reference.referencia_fk

        part_reference.delete()

        log_activity(
            user=request.user.id,
            action='DELETE',
            description=f'El usuario eliminó la asociación entre la pieza {part} y la referencia {reference}.',
            category='PARTS'
        )
        messages.success(request, 'Asociacion eliminada correctamente.')
        return JsonResponse({'success': True}, status=200) 
    
    except Exception:
        messages.error(request, 'Ocurrió un error inesperado.')
        return JsonResponse({'success': True})  
    
from django.http import JsonResponse, Http404

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators', 'technicians'], redirect_url='/forbidden_access/')
def new_part_reference(request):
    try:
        part_id = request.POST.get('partId')
        reference_id = request.POST.get('reference')

        try:
            part = get_object_or_404(Inventario, pk=part_id)
        except Http404:
            return JsonResponse({'error': 'No se encontró la pieza especificada.'})

        try:
            reference = get_object_or_404(Referencias, pk=reference_id)
        except Http404:
            return JsonResponse({'error': 'No se encontró la referencia especificada.'})

        if PiezasReferencias.objects.filter(num_parte_fk=part, referencia_fk=reference).exists():
            return JsonResponse({'error': 'La asociación ya existe.'})

        new_part_reference = PiezasReferencias.objects.create(
            num_parte_fk=part,
            referencia_fk=reference
        )

        log_activity(
            user=request.user.id,
            action='CREATE',
            description=f'El usuario creó una asociación entre la pieza {part} y la referencia {reference}.',
            link=f'/edit_part/{part.num_parte_pk}',
            category='PARTS'
        )

        messages.success(request, 'Asociación creada correctamente.')
        return JsonResponse({'success': True}, status=200)

    except Exception:
        messages.error(request, 'Ocurrió un error inesperado.')
        return JsonResponse({'success': True})

    



    

    

    