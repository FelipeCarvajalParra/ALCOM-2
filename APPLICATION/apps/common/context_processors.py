# yourapp/context_processors.py

def user_role_context(request):
    user = request.user
    role = 'No role'

    if user.is_authenticated:
        if user.groups.filter(name='administrators').exists():
            role = 'admin'
        elif user.groups.filter(name='technicians').exists():
            role = 'technician'
        elif user.groups.filter(name='consultants').exists():
            role = 'consultant'

        user_name = user.get_full_name() or "No name"
    else:
        user_name = "No name"

    return {
        'role': role,
        'user_name': user_name,
    }

def current_path(request):
    return {
        'current_path': request.path,
        'current_view': request.resolver_match.view_name,  # Obtén el nombre de la vista
    }