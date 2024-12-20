from django.urls import path
from . import views

urlpatterns = [
    path("new_equipment/", views.new_equipment , name="new_equipment"),
    path("delete_equipment/<id_equipment>", views.delete_equipment , name="new_equipment"),
    path("view_equipments/", views.view_equipments , name="view_equipments"),
    path("edit_equipment/<id_equipment>", views.edit_equipment , name="edit_equipment"),
    path("edit_equipment_state/", views.edit_equipment_state , name="edit_equipment_state"),
]
