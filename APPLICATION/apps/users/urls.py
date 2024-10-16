from django.urls import path
from . import views

urlpatterns = [
    path("view_users/", views.view_users, name="view_users"),
    path("register_user/", views.register_user, name="register_user"),
    path("edit_user/<id>", views.edit_user, name="edit_user"),
    path("update_personal_data/<user_id>", views.update_personal_data, name='update_personal_data'),
    path('update_login_data/<user_id>', views.update_login_data, name='update_login_data'),
    path('update_image/', views.update_image, name='update_image'),
    path('delete_user/<user_id>', views.delete_user, name='delete_user'),
]