from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('administrativo@alcomsas/', admin.site.urls),
    path('', include('apps.logIn.urls')),
    path('', include('apps.core.urls')),
    path('', include('apps.userProfile.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.categories.urls')),
    path('', include('apps.activityLog.urls')),
    path('', include('apps.references.urls')),
    path('', include('apps.files.urls')),
    path('', include('apps.equipments.urls')),
    path('', include('apps.errors.urls')),
    path('', include('apps.partsInventory.urls')),
    path('', include('apps.inserts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)