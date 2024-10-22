from django.urls import path
from . import views

urlpatterns = [
    path('update_file/', views.update_file, name='update_file'),
    path('delete_file/', views.delete_file, name='delete_file'),
    path('download_file/', views.download_file, name='download_file'),
]