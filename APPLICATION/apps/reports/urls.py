from django.urls import path
from . import views

urlpatterns = [
    path("view_reports/", views.view_reports, name='view_reports'),
]