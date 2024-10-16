from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home , name="home"),
    path("home/construction", views.site_construction , name="home/construction"),
    path("error_export", views.error_export, name='error_export')
]
