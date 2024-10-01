from django.urls import path, include
from . import views as views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('django.contrib.auth.urls')),
    path('redirect_user/', views.redirect_user, name="redirect_user"),
    path('validate_login/', views.login_validate, name='validate_login'),
    path('expired_session/', views.expired_session, name='expired_session'),
    path('', views.logout_user, name='logout_user')
]
