from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.db import transaction
import json
import os
from django.conf import settings
from django.core.paginator import Paginator
from apps.categories.models import Categorias, CategoriasCampo, Campo
from apps.equipments.models import Equipos
from .models import Valor, Referencias, Archivos
from apps.activityLog.utils import log_activity
from apps.logIn.views import group_required
from django.core.exceptions import ObjectDoesNotExist

default_image = f"{settings.MEDIA_URL}default/default.jpg"

@login_required
def view_references(request, id_category):

    search_query = request.GET.get('search', '').strip()
    filter_brand = request.GET.get('brand', '')

    references_list = Referencias.objects.filter(categoria=id_category).all().order_by('-referencia_pk')
    category_name = get_object_or_404(Categorias, pk=id_category).nombre
    components = CategoriasCampo.objects.filter(categoria_fk=id_category)
    brands = Referencias.objects.values('marca').distinct()
    default_image = os.path.join(settings.MEDIA_URL, 'default/default.jpg')

    if search_query:
        references_list = references_list.filter(referencia_pk__icontains=search_query)

    if filter_brand and filter_brand != 'TODAS':
        references_list = references_list.filter(marca=filter_brand)
    
    paginator = Paginator(references_list,5)  # Número de elementos por página
    page_number = request.GET.get('page')
    references_list = paginator.get_page(page_number)

    context = {
        'paginator': references_list,
        'category_name': category_name, 
        'components': components, 
        'id_category': id_category, 
        'brands': brands,
        'default_image': default_image
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_references_table_body.html', context, request=request)
        html_footer = render_to_string('partials/_references_table_footer.html', context, request=request)
        return JsonResponse({'body': html_body, 'footer': html_footer})

    return render(request, 'view_references.html', context)

@login_required
@require_POST
@transaction.atomic
def new_reference(request, category_id):
    try:
        data = json.loads(request.body)

        reference_pk = data.get('reference', '').strip()
        brand = data.get('brand', '').strip()
        url = data.get('url', '').strip()
        accessories = data.get('accessories', '').strip()
        observations = data.get('observations', '').strip()
        components = data.get('components', [])

        print('aqui:', components)

        # Verificar si la referencia ya existe
        if Referencias.objects.filter(referencia_pk=reference_pk).exists():
            return JsonResponse({'error': 'La referencia ya existe.'}, status=400)

        # Crear la referencia y valores dentro de una transacción
        category = get_object_or_404(Categorias, pk=category_id)
        new_reference = Referencias.objects.create(
            referencia_pk=reference_pk,
            categoria=category,
            marca=brand.upper(),
            accesorios=accessories,
            observaciones=observations,
            url_consulta=url
        )

        # Guardar los valores asociados a los campos
        for component in components:
            field_id = component.get('campoId')
            field_value = component.get('valor', '').strip()

            field = get_object_or_404(Campo, pk=field_id)
            
            # Crear el valor asociado sin importar si field_value está vacío
            Valor.objects.create(
                referencia_fk=new_reference,
                campo_fk=field,
                valor=field_value  # Se guarda aunque esté vacío
            )
        
        new_files_instance = Archivos.objects.create(
            referencia_pk=get_object_or_404(Referencias, pk=reference_pk)
        )

        # Registrar la actividad
        log_activity(
            user=request.user.id,
            action='CREATE',
            title='Registro de referencia',
            description=f'El usuario registró la referencia {reference_pk}.',
            link=f'/view_categories/view_references/{new_reference.referencia_pk}',
            category='USER_PROFILE'
        )

        messages.success(request, 'Referencia registrada correctamente')
        return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al procesar los datos.'}, status=400)
    except Campo.DoesNotExist:
        return JsonResponse({'error': 'Campo no encontrado.'}, status=404)
    except Categorias.DoesNotExist:
        return JsonResponse({'error': 'Categoría no encontrada.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@login_required
@require_POST
@transaction.atomic  # Asegura que todas las operaciones se realicen como una sola transacción
def delete_reference(request, reference_id):
    try:
        reference_instance = get_object_or_404(Referencias, pk=reference_id)

        # Verificar si hay archivos asociados
        try:
            archivos_instance = Archivos.objects.get(referencia_pk=reference_instance)

            # Eliminar imágenes
            for imagen in [archivos_instance.imagen_1, archivos_instance.imagen_2, archivos_instance.imagen_3, 
                           archivos_instance.imagen_4, archivos_instance.imagen_5]:
                if imagen and imagen.url != settings.MEDIA_URL + 'default/image_none.jpg':
                    image_path = imagen.path
                    if os.path.exists(image_path):
                        os.remove(image_path)

            # Eliminar ficha técnica
            if archivos_instance.ficha_tecnica:
                ficha_path = archivos_instance.ficha_tecnica.path
                if os.path.exists(ficha_path):
                    os.remove(ficha_path)

            # Eliminar el registro de archivos
            archivos_instance.delete()

        except Archivos.DoesNotExist:
            pass
        
        log_activity(  
            user=request.user.id,                       
            action='DELETE',                 
            title='Elimino referencia',      
            description=f'El usuario elimino la referencia {reference_instance.referencia_pk}.',  
            category='REFERENCE'          
        )

        reference_instance.delete() #Primero la actividad luego la accion por el atomic
        messages.success(request, 'Referencia eliminada correctamente.')
        return HttpResponse(status=200)  # Respuesta exitosa
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponse(status=500)  # Error interno en el servidor
    
def edit_reference(request, reference_id):
  
    reference = get_object_or_404(Referencias, pk=reference_id)
    category_id = reference.categoria
    components = CategoriasCampo.objects.filter(categoria_fk=category_id)
    brands = Referencias.objects.values('marca').distinct()
    list_equipments = Equipos.objects.filter(referencia_fk = reference_id)
    
    components_with_values = []  # asociar campos con los valores correspondientes
    for component in components:
        campo_id = component.campo_fk.campo_pk  
        valor = Valor.objects.filter(referencia_fk=reference_id, campo_fk=campo_id).first()
        if valor:
            component.valor = valor.valor
            component.valor_id = valor.id_pk  # Aquí estamos agregando el ID de la tabla valor
        else:
            component.valor = ""
            component.valor_id = None  # Asignar None si no hay valor
        components_with_values.append(component)

    try:
        # Obtener la instancia de 'reference'
        reference = get_object_or_404(Referencias, pk=reference_id)  # Reemplaza con tu modelo
        
        try:
            archivos_obj = reference.archivos  
            data_sheet = archivos_obj.ficha_tecnica.url if archivos_obj.ficha_tecnica else None
        except Archivos.DoesNotExist:
            # Crear el objeto relacionado si no existe
            archivos_obj = Archivos.objects.create(referencia_pk=reference)
            data_sheet = archivos_obj.ficha_tecnica.url if archivos_obj.ficha_tecnica else None

    except Exception as e:
        return HttpResponse(f"Ocurrió un error: {str(e)}")
    

    context = {
        'reference': reference,
        'data_sheet': data_sheet,
        'components': components_with_values, 
        'default_image': default_image,
        'brands': brands,
        'list_equipments': list_equipments
    }
    
    # Renderiza la plantilla
    return render(request, 'edit_reference.html', context)


@login_required
@require_POST
@transaction.atomic
def edit_reference_data_general(request, reference_id):
    try:
        reference = get_object_or_404(Referencias, pk=reference_id)
        
        fields = {
            'referencia_pk': request.POST.get('reference'),
            'marca': request.POST.get('brand'),
            'url_consulta': request.POST.get('url'),  # Cambiado aquí
            'accesorios': request.POST.get('accessories'),  
            'observaciones': request.POST.get('observations')
        }

        new_reference_code = fields.get('referencia_pk')
        if new_reference_code and new_reference_code != reference.referencia_pk:
            if Referencias.objects.filter(referencia_pk=new_reference_code).exclude(pk=reference_id).exists():
                return JsonResponse({'error': 'El código de referencia ya existe.'}, status=400)
        
        # Actualizar los campos
        for field, value in fields.items():
            if value: 
                setattr(reference, field, value)
        
        reference.save()  # Guardar los cambios

        messages.success(request, 'Datos generales actualizados correctamente.')
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': 'Ha ocurrido un error inesperado.'}, status=500)


@login_required
@require_POST
@transaction.atomic
def edit_reference_components(request, reference_id):
    
    reference = get_object_or_404(Referencias, pk=reference_id)

    # Recorre los datos POST para encontrar los valores
    for key, value in request.POST.items():
        if key.startswith('valor_'):  # Identifica los campos que coincidan con el prefijo
            try:
                valor_id = key.split('_')[1]  # Extrae el ID del valor del nombre del campo
                valor_obj = Valor.objects.get(pk=valor_id, referencia_fk=reference_id)
                valor_obj.valor = value  # Actualiza el valor con el nuevo texto
                valor_obj.save()  # Guarda el cambio
            except Valor.DoesNotExist:
                return JsonResponse({'error': f'El valor con ID {valor_id} no existe.'}, status=400)
            except Exception as e:
                return JsonResponse({'error': 'Ha ocurrido un error inesperado.'}, status=500)

    messages.success(request, 'Datos generales actualizados correctamente.')
    return JsonResponse({'success': True})
    
  