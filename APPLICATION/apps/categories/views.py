from django.shortcuts import render

# Create your views here.
def view_categories(request):
    return render(request, 'view_categories.html')