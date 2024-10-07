from .models import ActivityLog
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import HttpResponse

def delete_activity_log(request, id_log):
    if request.method == 'POST':
        try:
            log = get_object_or_404(ActivityLog, pk=id_log)
            log.delete() 
            messages.success(request, 'Registro eliminado correctamente')
            return HttpResponse(status=200)
        except Exception as e:
            messages.error(request, f'Error al eliminar el registro: {str(e)}')
            return HttpResponse(status=500)
    else:
        return redirect('view_users')