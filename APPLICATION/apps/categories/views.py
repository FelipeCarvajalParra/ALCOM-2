from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Categorias, Campo, CategoriasCampo
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from apps.logIn.views import group_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from apps.activityLog.utils import log_activity


@login_required
@group_required(['administrators'], redirect_url='expired_session')
def view_categories(request):
    categories_list = Categorias.objects.annotate(num_equipos=Count('referencias')).all()
    search_query = request.GET.get('search', '')
    components = Campo.objects.all()

    
    if search_query:
        categories_list = categories_list.filter(nombre__icontains=search_query)

    paginator = Paginator(categories_list, 13) #paginacion
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'components': components
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/_category_table_body.html', context, request=request)
        return HttpResponse(html)

    
    return render(request, 'view_categories.html', context)

@login_required
@group_required(['administrators'], redirect_url='expired_session')
def new_category(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name_category = data.get('nameCategory', '').strip().capitalize()
            if Categorias.objects.filter(nombre=name_category).exists():
                return JsonResponse({'error': 'La categoría ya existe.'}, status=400)
            categoria = Categorias.objects.create(nombre=name_category)

            components = data.get('components', [])
            # Lista para almacenar campos creados o existentes
            for component_name in components:
            
                component_name = component_name.strip().capitalize()
                campo, created = Campo.objects.get_or_create(nombre_campo=component_name)
                CategoriasCampo.objects.create(categoria_fk=categoria, campo_fk=campo)

            
            log_activity(
                user=request.user.id,                       
                action='CREATE',                 
                title='Registro de categoria',      
                description=f'El usuario registro la categoria {categoria.nombre} en el sistema.',  
                link=f'/view_categories/view_references/{categoria.categoria_pk}',      
                category='USER_PROFILE'          
            )
            messages.success(request, 'Categoría y campos asociados correctamente.')
            return JsonResponse({'success': True}, status=200)  

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar los datos.'}, status=400)  
        except Exception as e:
            messages.error(request, 'Error: ' + str(e))
            return JsonResponse({'error': 'Ocurrió un error: ' + str(e)}, status=500)  

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@login_required
@group_required(['administrators'], redirect_url='expired_session')
def get_category(request, category_id):
    try:
        
        category = Categorias.objects.get(pk=category_id)
        campos = Campo.objects.filter(categoriascampo__categoria_fk=category)  # Obtener campos asociados

        campos_data = [{'nombre_campo': campo.nombre_campo} for campo in campos]

        return JsonResponse({
            'categoria_pk': category.categoria_pk,
            'nombre': category.nombre,
            'campos': campos_data
        })
        

    except Categorias.DoesNotExist:
        return JsonResponse({'error': 'Categoría no encontrada.'})


@login_required
@group_required(['administrators'], redirect_url='expired_session')
def update_category(request, category_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Obtener el nuevo nombre de la categoría
            name_category = data.get('nameCategory', '').strip().capitalize()
            # Validar que el nombre de la categoría no esté repetido
            if Categorias.objects.filter(nombre=name_category).exclude(categoria_pk=category_id).exists():
                return JsonResponse({'error': 'La categoría ya existe.'}, status=400)

            # Actualizar la categoría
            categoria = Categorias.objects.get(categoria_pk=category_id)
            categoria.nombre = name_category
            categoria.save()

            # Obtener componentes del formulario
            components = data.get('components', [])

            # Actualizar la relación de campos
            existing_components = [campo.campo_fk.nombre_campo for campo in CategoriasCampo.objects.filter(categoria_fk=categoria)]
            new_components = []

            for component_name in components:
                component_name = component_name.strip().capitalize()
                campo, created = Campo.objects.get_or_create(nombre_campo=component_name)
                new_components.append(campo)

                # Si el campo no existía, se crea una nueva relación
                if campo not in existing_components:
                    CategoriasCampo.objects.get_or_create(categoria_fk=categoria, campo_fk=campo)

            # Eliminar relaciones de CategoriasCampo para campos que ya no están
            for component in existing_components:
                if component not in components:
                    campo = Campo.objects.get(nombre_campo=component)
                    CategoriasCampo.objects.filter(categoria_fk=categoria, campo_fk=campo).delete()

            messages.success(request, 'Categoría y campos actualizados correctamente.')
            return JsonResponse({'success': True}, status=200)  

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar los datos.'}, status=400)
        except Exception as e:
            messages.error(request, 'Error: ' + str(e))
            return JsonResponse({'error': 'Ocurrió un error: ' + str(e)}, status=500)  

    return JsonResponse({'error': 'Método no permitido.'}, status=405)


def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            # Obtener y eliminar la categoría
            categoria = Categorias.objects.get(categoria_pk=category_id)
            categoria.delete()

            messages.success(request, 'Categoría eliminada correctamente')
            return JsonResponse({'success': True}, status=200)  
        except Categorias.DoesNotExist:
            messages.error(request, 'La categoría no existe.')
            return JsonResponse({'success': True}, status=404)  
        except Exception as e:
            messages.error(request, 'Ocurrió un error: ' + str(e))
            return JsonResponse({'success': True}, status=404)  

    messages.error(request, 'Metodo no permitido.')
    return JsonResponse({'success': True}, status=404)  