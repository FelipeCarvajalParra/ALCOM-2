from .models import ActivityLog
from django.shortcuts import get_object_or_404
from apps.users.models import CustomUser

def log_activity(user, action, title, description, link=None, category=None):

    user = get_object_or_404(CustomUser, pk=user)

    ActivityLog.objects.create(
        user=user,
        action=action,
        title=title,
        description=description,
        link=link,
        category=category
    )
