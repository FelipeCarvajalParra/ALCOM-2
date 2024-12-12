from django.urls import path
from . import views

urlpatterns = [
    path('new_shopping/', views.new_shopping, name="new_shopping"),
    path('delete_shopping/<shopping_id>', views.delete_shopping, name="delete_shopping"),
    path('validate_shopping/<shopping_id>', views.validate_shopping, name="validate_shopping"),
    path('consult_shopping/<shopping_id>', views.consult_shopping, name="consult_shopping"),
]