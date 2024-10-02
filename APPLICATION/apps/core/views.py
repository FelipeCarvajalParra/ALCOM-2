from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user_groups = {
        'is_admin': request.user.groups.filter(name='Administrators').exists(),
        'is_consultant': request.user.groups.filter(name='Consultants').exists(),
        'is_technician': request.user.groups.filter(name='Technicians').exists(),
    }

    context = {
        'user_groups': user_groups,
    }

    return render(request, 'home.html', context)
