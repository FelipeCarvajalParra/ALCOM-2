from django.urls import path
from . import views
from apps.references.views import view_references


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("new_reference/<category_id>", views.new_reference, name="new_reference"),
    path("delete_reference/<reference_id>", views.delete_reference, name='delete_reference'),
    path("edit_reference/<reference_id>", views.edit_reference, name='edit_reference')
]