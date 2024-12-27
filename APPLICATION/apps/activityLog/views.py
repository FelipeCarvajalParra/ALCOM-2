from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from .models import ActivityLog
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction
from apps.logIn.views import group_required
from apps.users.models import CustomUser

@login_required
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def view_activity(request):

    activity = ActivityLog.objects.all().order_by('-timestamp')

    map_category = {
        'Categorias': 'CATEGORY',
        'Referencias': 'REFERENCE',
        'Equipos': 'EQUIPMENT',
        'Intervenciones': 'INTERVENTION',
        'Usuarios': 'USER',
        'Cuentas': 'ACCOUNT',
    }

    category = request.GET.get('category')
    if category and category != 'TODAS' and category != 'Categoria':
        activity = activity.filter(category=map_category.get(category, None))

    date_range = request.GET.get('dateRange')
    if date_range:
        try:
            start_date_str, end_date_str = date_range.split(' - ')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
            
            # Añade la zona horaria
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())
            
            # Filtrar por rango de fechas
            activity = activity.filter(timestamp__range=(start_date, end_date))
        except (ValueError, IndexError):
            pass

    search_query = request.GET.get('search', '').strip()
    if search_query:
        activity = activity.filter(description__icontains=search_query)

    paginator = Paginator(activity, 15)
    page_number = request.GET.get('page')
    paginator = paginator.get_page(page_number)

    context = {
        'paginator': paginator,
        'page_number': page_number,
        'category': category,
        'date_range': date_range,
        'search_query': search_query,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_body = render_to_string('partials/_view_activity_table_body.html', context, request=request)
        html_footer = render_to_string('partials/_view_activity_table_footer.html', context, request=request)
        return JsonResponse({'body': html_body, 'footer': html_footer})

    return render(request, 'view_activity.html', context)

@login_required
@require_POST
@transaction.atomic
@group_required(['administrators'], redirect_url='/forbidden_access/')
def delete_activity_log(request, id_log):
    try:
        log = get_object_or_404(ActivityLog, pk=id_log)
        log.delete() 
        messages.success(request, 'El registro ha sido eliminado correctamente.')
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error al eliminar el registro: {str(e)}')
        return HttpResponse(status=500)