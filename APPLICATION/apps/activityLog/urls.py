from django.urls import path
from . import views

urlpatterns = [
    path("view_activity/", views.view_activity, name="view_activity"),
    path("delete_log_activity/<id_log>", views.delete_activity_log, name="delete_log_activity"),
]