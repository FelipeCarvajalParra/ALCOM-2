from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from .models import ActivityLog
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
def view_activity(request):

    activity = ActivityLog.objects.all()

    context = {
        'activity': activity
    }

    return render(request, 'view_activity.html', context)

@require_POST
@login_required
def delete_activity_log(request, id_log):
    try:
        log = get_object_or_404(ActivityLog, pk=id_log)
        log.delete() 
        messages.success(request, 'El registro ha sido eliminado correctamente.')
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error al eliminar el registro: {str(e)}')
        return HttpResponse(status=500)
    
