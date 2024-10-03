from django.urls import path, include
from . import views as views

urlpatterns = [
    path('profile/', views.profile_user, name='profile'),
]
