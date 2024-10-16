from django.shortcuts import render, get_object_or_404, redirect
from apps.categories.models import Categorias, CategoriasCampo, Campo
from .models import Valor
from .models import Referencias
import json
from django.http import JsonResponse
from apps.activityLog.utils import log_activity
from django.contrib import messages
from django.db import transaction

def view_references(request, id_category):
    references_list = Referencias.objects.filter(categoria=id_category)
    category_name = get_object_or_404(Categorias, pk=id_category).nombre
    components = CategoriasCampo.objects.filter(categoria_fk=id_category)
    brands = Referencias.objects.values('marca').distinct()

    context = {
        'reference_list': references_list,
        'category_name': category_name, 
        'components': components, 
        'id_category': id_category, 
        'brands': brands
    }

    return render(request, 'view_references.html', context)

def new_reference(request, category_id):
    if request.method == 'POST':
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
                    marca= brand.UPPER(),
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
        except Exception:
            return JsonResponse({'error': 'Ocurrió un error inesperado.'}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)


