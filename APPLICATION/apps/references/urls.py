from django.urls import path
from . import views

urlpatterns = [
    path("new_reference/<path:category_id>", views.new_reference, name="new_reference"),
    path("delete_reference/<path:reference_id>", views.delete_reference, name='delete_reference'),
    path("edit_reference/<path:reference_id>", views.edit_reference, name='edit_reference'),
    path("edit_reference_data_general/<path:reference_id>", views.edit_reference_data_general, name='edit_reference_data_general'),
    path("edit_reference_components/<path:reference_id>", views.edit_reference_components, name='edit_reference_components'),
    path("view_all_references/", views.view_all_references, name='view_all_references')
]