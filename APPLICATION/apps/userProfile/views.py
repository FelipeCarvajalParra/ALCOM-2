from django.shortcuts import render
from apps.core.views import home

def profile_user(request):

    

    home(request)


    return render(request, 'profile.html')