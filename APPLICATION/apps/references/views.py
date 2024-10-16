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
from datetime import datetime
from apps.categories.models import Categorias, CategoriasCampo, Campo
from .models import Valor, Referencias, Archivos
from apps.activityLog.utils import log_activity
from apps.logIn.views import group_required

@login_required
def view_references(request, id_category):
    search_query = request.GET.get('search', '')
    filter_brand = request.GET.get('brand', '')

    references_list = Referencias.objects.filter(categoria=id_category)
    category_name = get_object_or_404(Categorias, pk=id_category).nombre
    components = CategoriasCampo.objects.filter(categoria_fk=id_category)
    brands = Referencias.objects.values('marca').distinct()

    if search_query:
        references_list = references_list.filter(referencia_pk__icontains=search_query)

    if filter_brand and filter_brand != 'TODAS':
        references_list = references_list.filter(marca=filter_brand)

    context = {
        'reference_list': references_list,
        'category_name': category_name, 
        'components': components, 
        'id_category': id_category, 
        'brands': brands
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/_references_table_body.html', context, request=request)
        return HttpResponse(html)

    return render(request, 'view_references.html', context)

@login_required
@require_POST
def new_reference(request, category_id):
    try:
        data = json.loads(request.body)

        reference_pk = data.get('reference', '').strip()
        brand = data.get('brand', '').strip()
        url = data.get('url', '').strip()
        accessories = data.get('accessories', '').strip()
        observations = data.get('observations', '').strip()
        components = data.get('components', [])

        # Verificar si la referencia ya existe
        if Referencias.objects.filter(referencia_pk=reference_pk).exists():
            return JsonResponse({'error': 'La referencia ya existe.'}, status=400)

        # Crear la referencia y valores dentro de una transacción
        with transaction.atomic():
            category = get_object_or_404(Categorias, pk=category_id)
            new_reference = Referencias.objects.create(
                referencia_pk=reference_pk,
                categoria=category,
                marca= brand.upper(),
                accesorios=accessories,
                observaciones=observations,
                url_consulta=url
            )

            # Guardar los valores asociados a los campos
            for component in components:
                field_id = component.get('campoId')
                field_value = component.get('valor', '').strip()

                if field_value:
                    field = get_object_or_404(Campo, pk=field_id)
                    Valor.objects.create(
                        referencia_fk=new_reference,
                        campo_fk=field,
                        valor=field_value
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
        return JsonResponse({'error': 'Ha ocurrido un error inesperado'}, status=500)



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