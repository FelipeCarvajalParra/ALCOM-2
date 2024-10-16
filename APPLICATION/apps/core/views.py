from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from apps.logIn.views import group_required
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.contrib import messages
from io import BytesIO


@login_required
def home(request):
    now = datetime.now()
    current_hour = now.hour

    if current_hour < 12:
        greeting = f'¡Buenos días {request.user.first_name}!'
    elif 12 <= current_hour < 18:
        greeting = f'¡Buenas tardes {request.user.first_name}¡'
    else:
        greeting = "¡Hola!"


    context = {
        'greeting': greeting
    }

    return render(request, 'home.html', context)



@login_required
def site_construction(request):
    return render(request, 'construction.html')



def error_export(request):
    messages.error(request, 'Usted no tiene permiso para generar reportes.')
    return redirect('view_categories')
