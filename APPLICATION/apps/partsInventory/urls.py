from django.urls import path
from . import views

urlpatterns = [
    path('view_inventory_parts/', views.view_inventory_parts, name="view_inventory_parts"),
    path('new_part/', views.new_part, name="new_part"),
    path('edit_part/<part_id>', views.edit_part, name="edit_part"),
    path('edit_part_action/<part_id>', views.edit_part_action, name="edit_part_action"),
]