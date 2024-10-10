from django.shortcuts import render, get_object_or_404
from apps.categories.models import Categorias  
from apps.equipments.models import Equipos

def view_references(request, id_category):

    references_list = Equipos.objects.filter(categoria=id_category)
    category_name = get_object_or_404(Categorias, pk=id_category).nombre

    context = {
        'reference_list': references_list,
        'category_name': category_name
    }

    return render(request, 'view_references.html', context)