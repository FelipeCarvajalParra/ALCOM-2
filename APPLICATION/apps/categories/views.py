from django.shortcuts import render
from django.db.models import Count
from apps.categories.models import Categorias
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string



def view_categories(request):
    # Obtener todas las categorías con el conteo de equipos
    categories_list = Categorias.objects.annotate(num_equipos=Count('equipos')).all()
    
    # Obtener la consulta de búsqueda
    search_query = request.GET.get('search', '')
    
    if search_query:
        categories_list = categories_list.filter(nombre__icontains=search_query)

    # Paginación
    paginator = Paginator(categories_list, 13)  # Ajusta el número de categorías por página
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)

    # Verifica si es una solicitud AJAX a través del encabezado HTTP
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/_category_table_body.html', {'categories': categories}, request=request)
        return HttpResponse(html)

    # Crear el contexto una sola vez
    context = {
        'categories': categories
    }

    return render(request, 'view_categories.html', context)