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

def section_highlighter_processor(request):
    current_path = request.path
    
    return {
        'is_home': current_path.startswith('/home/'),
        'is_profile': current_path.startswith('/profile/'),
        'is_view_user': current_path.startswith('/view_users/'),
        'is_activity': current_path.startswith('/view_activity/'),
        'is_edit_user': current_path.startswith('/edit_user/'),
        'is_view_category': current_path.startswith('/view_categories/'),
        'is_view_equipments': current_path.startswith('/view_equipments/'),
        'is_view_references': current_path.startswith('/view_all_references/'),
        'is_inventory_parts': current_path.startswith('/view_inventory_parts/'),
        'is_edit_part': current_path.startswith('/edit_part/'),
        'is_view_interventions': current_path.startswith('/view_interventions/'),
        'is_edit_equipment': current_path.startswith('/edit_equipment/'),
        'is_order_service': current_path.startswith('/order_service/'),
    }