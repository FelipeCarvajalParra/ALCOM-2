from django.urls import path
from . import views
from apps.references.views import view_references

urlpatterns = [
    path("view_categories/", views.view_categories, name="view_categories"),
    path("view_categories/view_references/<id_category>", view_references, name="view_references"),
    path("new_categorie/", views.new_category, name="new_categorie"),
    path("get_category/<category_id>", views.get_category, name="get_category"),
    path("update_category/<category_id>", views.update_category, name="update_category"),
    path("delete_category/<category_id>", views.delete_category, name='delete_category')
]