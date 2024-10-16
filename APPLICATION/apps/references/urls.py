from django.urls import path
from . import views
from apps.references.views import view_references

urlpatterns = [
    path("new_reference/<category_id>", views.new_reference , name="new_reference"),
]