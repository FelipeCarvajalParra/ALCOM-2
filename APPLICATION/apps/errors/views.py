from django.shortcuts import render, redirect

# Create your views here.
def forbidden_access(request):
    return render(request, '403.html', status=403)