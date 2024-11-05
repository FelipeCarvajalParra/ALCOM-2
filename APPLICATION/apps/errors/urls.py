from django.urls import path
from . import views

urlpatterns = [
     path('forbidden_access/', views.forbidden_access, name='forbidden_access')
]