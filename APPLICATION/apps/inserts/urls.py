from django.urls import path
from . import views

urlpatterns = [
    path('add_parts/<part_id>', views.add_parts, name="add_parts"),
]