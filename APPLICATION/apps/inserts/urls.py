from django.urls import path
from . import views

urlpatterns = [
    path('add_parts/<part_id>', views.add_parts, name="add_parts"),
    path('consult_movements/<movement_id>', views.consult_movements, name="consult_movements"),
    path('consult_interventions/<intervention_id>', views.consult_interventions, name="consult_interventions"),
    path('view_interventions', views.view_interventions, name="view_interventions"),
]