from django.urls import path, include
from . import views as views
from apps.core.views import site_construction

urlpatterns = [
    path('profile/', views.profile_user, name='profile'),
    path('profile/construction', site_construction, name='profile/construction'),
]
