from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name=""),
    path("home/", views.home , name="home"),
    path("home/construction", views.site_construction , name="home/construction"),
    path("search_general/", views.search_general, name='search_general'),
]
