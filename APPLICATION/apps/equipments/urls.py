from django.urls import path
from . import views

urlpatterns = [
    path("new_equipment/", views.new_equipment , name="new_equipment"),
]
