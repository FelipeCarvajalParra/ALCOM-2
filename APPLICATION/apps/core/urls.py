from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home , name="home"),
    path("home/construction", views.site_construction , name="home/construction"),
]
