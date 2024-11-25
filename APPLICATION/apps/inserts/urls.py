from django.urls import path
from . import views

urlpatterns = [
    path('add_parts/<part_id>', views.add_parts, name="add_parts"),
    path('consult_movements/<movement_id>', views.consult_movements, name="consult_movements"),
    path('consult_interventions/<intervention_id>', views.consult_interventions, name="consult_interventions"),
    path('view_interventions', views.view_interventions, name="view_interventions"),
    path('new_intervention/', views.new_intervention, name="new_intervention"),
    path('create_orden/', views.create_orden, name="create_orden"),
]