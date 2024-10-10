from django.urls import path
from . import views
from apps.references.views import view_references

urlpatterns = [
    path("view_categories/", views.view_categories, name="view_categories"),
    path("view_categories/view_references/<id_category>", view_references, name="view_references"),
]