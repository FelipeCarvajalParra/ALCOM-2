from django.urls import path
from . import views

urlpatterns = [
    path("new_goat/", views.new_goat, name="new_goat"),
    path("delete_goal/<int:id>", views.delete_goal, name="delete_goal"),
]