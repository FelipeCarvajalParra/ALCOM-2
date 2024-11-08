from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
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

default_image = f"{settings.MEDIA_URL}default/default.jpg"

@login_required
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
def new_part(request):
    partNumber = request.POST.get('partNumber')
    stock = request.POST.get('stock')
    namePart = request.POST.get('namePart')
    location = request.POST.get('location')

    print(partNumber, stock, namePart, location)

    if not partNumber or not stock or not namePart or not location:
        return JsonResponse({'error': 'Todos los campos son obligatorios.'})

    if Inventario.objects.filter(pk=partNumber).exists():
        return JsonResponse({'error': 'El número de parte ya existe.'})

    if not stock.isdigit():
        return JsonResponse({'error': 'El valor en unidades debe ser un número entero.'})
    stock = int(stock)  # Convierte `stock` a entero después de la validación

    try:
        new_part = Inventario.objects.create(
            num_parte_pk=partNumber,
            nombre=namePart,
            ubicacion=location,
            total_unidades=stock,
        )

    except Exception as e:
        return JsonResponse({'error':'Error inesperado'})

    messages.success(request, 'Pieza registrada correctamente')
    return JsonResponse({'success': True})


def edit_part(request, part_id):

    part = get_object_or_404(Inventario, pk=part_id)
    part_movements = Actualizaciones.objects.filter(num_parte_fk=part_id).order_by('-actualizacion_pk')


    paginator = Paginator(part_movements,15) 
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'part': part,
        'default_image': default_image,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_category_table_body.html', context, request=request)
        html_footer = render_to_string('partials/_category_table_footer.html', context, request=request)
        return JsonResponse({'body': html_body, 'footer': html_footer})

    return render(request, 'edit_part.html', context)






@login_required
@require_POST
@transaction.atomic
def edit_part_action(request, part_id):
    try:
        part = Inventario.objects.get(num_parte_pk=part_id)
        namePart = request.POST.get('namePart')
        location = request.POST.get('location')
        url = request.POST.get('url')

        print( "nombre: ", namePart,  "locacion: ", location,  "url: ", url)

        part.nombre = namePart
        part.ubicacion = location
        part.link_consulta = url

        part.save()
  
        messages.success(request, 'Pieza actualizada correctamente.')
        return JsonResponse({'succes': True})

    except Inventario.DoesNotExist:
        return JsonResponse({'error':'No se encontro el registro'})
    except Exception as e:
        return JsonResponse({'error':f'Error inesperado {e}'})



    



    

    

    