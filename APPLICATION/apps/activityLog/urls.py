from django.urls import path
from . import views

urlpatterns = [
    path("delete_log_activity/<id_log>", views.delete_activity_log, name="delete_log_activity"),
]