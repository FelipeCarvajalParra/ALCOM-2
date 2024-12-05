from django.shortcuts import render, redirect

# Create your views here.
def forbidden_access(request, message=None):

    if not message:
        message = 'Usted no tiene permiso para acceder a esta página.'

    context = {
        'message': message
    }

    return render(request, '403.html', context, status=403)