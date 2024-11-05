from django.shortcuts import render

# Create your views here.
def forbidden_access(request):
    return render(request, '403.html')