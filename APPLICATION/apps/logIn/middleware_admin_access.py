# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class RestrictAdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica si el usuario está intentando acceder al admin
        if request.path.startswith('/admin/'):
            if request.user.is_authenticated:
                # Verifica si el usuario pertenece al grupo específico
                if request.user.groups.filter(name='consultants').exists():
                    return redirect(reverse('expired_session'))
        return self.get_response(request)
