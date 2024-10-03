from django.urls import path
from . import views

urlpatterns = [
    path("view_users/", views.view_users, name="view_users"),
    path("edit_user/<id>", views.edit_user, name="edit_user"),
]