from django.urls import path, include
from . import views as views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('django.contrib.auth.urls')),
    path('redirect_user/', views.redirect_user, name="redirect_user"),
    path('login_validate/', views.login_validate, name='login_validate'),
    path('expired_session/', views.expired_session, name='expired_session'),
    path('', views.logout_user, name='logout_user')
]
