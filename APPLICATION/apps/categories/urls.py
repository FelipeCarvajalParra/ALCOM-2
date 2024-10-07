from django.urls import path
from . import views

urlpatterns = [
    path("view_categories/", views.view_categories, name="view_categories"),
]