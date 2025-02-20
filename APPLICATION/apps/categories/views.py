from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
import json
from apps.logIn.views import group_required
from .models import Categorias, Campo, CategoriasCampo
from apps.activityLog.utils import log_activity
from apps.references.models import Valor, Referencias

@login_required
@group_required(['administrators', 'technicians'], redirect_url='/forbidden_access/')
def view_categories(request):
    categories_list = Categorias.objects.annotate(num_equipos=Count('referencias')).all().order_by('-categoria_pk')
    search_query = request.GET.get('search', '')
    components = Campo.objects.all()

    if search_query:
        categories_list = categories_list.filter(nombre__icontains=search_query)

    paginator = Paginator(categories_list,15) 
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'components': components,
        'search_query': search_query,  # Agrega el término de búsqueda al contexto
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_category_table_body.html', context, request=request)
        html_footer = render_to_string('partials/_category_table_footer.html', context, request=request)
        return JsonResponse({'body': html_body, 'footer': html_footer})
    
    return render(request, 'view_categories.html', context)

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def new_category(request):
    try:
        data = json.loads(request.body)
        name_category = data.get('nameCategory', '').strip().capitalize()

        # Verificar si la categoría ya existe
        if Categorias.objects.filter(nombre=name_category).exists():
            return JsonResponse({'error': 'La categoría ya existe.'}, status=400)
       
        categoria = Categorias.objects.create(nombre=name_category)

        components = data.get('components', [])
        for component_name in components:
            component_name = component_name.strip().capitalize()
            campo, created = Campo.objects.get_or_create(nombre_campo=component_name)
            CategoriasCampo.objects.create(categoria_fk=categoria, campo_fk=campo)

        log_activity(
            user=request.user.id,                       
            action='CREATE',                    
            description=f'El usuario registro la categoria {categoria.nombre}.',  
            link=f'/view_categories/view_references/{categoria.categoria_pk}',
            category='CATEGORY'          
        )
        messages.success(request, 'Categoría y campos asociados correctamente.')
        return JsonResponse({'success': True}, status=201)  # 201 Created

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al procesar los datos.'}, status=400)
    except Exception:
        return JsonResponse({'error': 'Ocurrió un error inesperado.'}, status=500)

@login_required
@transaction.atomic
@group_required(['administrators', 'technicians'], redirect_url='/forbidden_access/')
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
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def update_category(request, category_id):
    try:
        data = json.loads(request.body)

        name_category = data.get('nameCategory', '').strip().capitalize()
        if Categorias.objects.filter(nombre=name_category).exclude(categoria_pk=category_id).exists():
            return JsonResponse({'error': 'La categoría ya existe.'}, status=400)

        # Actualizar la categoría
        categoria = Categorias.objects.get(categoria_pk=category_id)
        categoria.nombre = name_category
        categoria.save()

        components = data.get('components', [])  # Obtener componentes del formulario

        # Obtener todas las referencias de la categoría
        referencias = Referencias.objects.filter(categoria=categoria)

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

                # Crear una instancia vacía en Valor para cada referencia asociada
                for referencia in referencias:
                    Valor.objects.get_or_create(referencia_fk=referencia, campo_fk=campo)

        # Eliminar relaciones de CategoriasCampo para campos que ya no están
        for component in existing_components:
            if component not in components:
                campo = Campo.objects.get(nombre_campo=component)
                CategoriasCampo.objects.filter(categoria_fk=categoria, campo_fk=campo).delete()

                # Eliminar instancias de Valor asociadas a este campo solo si la referencia no tiene este campo
                for referencia in referencias:
                    # Verificar si existe la relación en CategoriasCampo
                    if not CategoriasCampo.objects.filter(categoria_fk=referencia.categoria, campo_fk=campo).exists():
                        Valor.objects.filter(campo_fk=campo, referencia_fk=referencia).delete()

        log_activity(
            user=request.user.id,                       
            action='UPDATE',                    
            description=f'El usuario edito la categoria {categoria.nombre}.',  
            link=f'/view_categories/view_references/{categoria.categoria_pk}',
            category='CATEGORY'          
        )
        messages.success(request, 'Categoría y campos actualizados correctamente.')
        return JsonResponse({'success': True}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al procesar los datos.'}, status=400)
    except Exception as e:
        messages.error(request,'Error inesperado')
        return JsonResponse({'error':'Error inesperado'}) 

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def delete_category(request, category_id):
    try:
        # Obtener y eliminar la categoría
        categoria = Categorias.objects.get(categoria_pk=category_id)
        categoria.delete()

        log_activity(
            user=request.user.id,                       
            action='DELETE',                    
            description=f'El usuario elimino la categoria {categoria.nombre}.',  
            category='CATEGORY'          
        )
        messages.success(request, 'Categoría eliminada correctamente.')
        return JsonResponse({'success': True}, status=200) 
    
    except Categorias.DoesNotExist:
        messages.error(request, 'La categoría no existe.')
        return JsonResponse({'success': True}, status=500)  
    except Exception as e:
        messages.error(request, 'Ocurrió un error: ' + str(e))
        return JsonResponse({'success': True}, status=500)  

