from django.urls import path, include
from . import views as views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('login_validate/', views.login_validate, name='login_validate'),
    path('logout_user/', views.logout_user, name='logout_user')
]
