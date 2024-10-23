from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.logIn.urls')),
    path('', include('apps.core.urls')),
    path('', include('apps.userProfile.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.categories.urls')),
    path('', include('apps.activityLog.urls')),
    path('', include('apps.references.urls')),
    path('', include('apps.files.urls')),
    path('', include('apps.equipments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)