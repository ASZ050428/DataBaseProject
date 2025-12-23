from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.UserView import (
    RegisterView,
    MeView,
    ChangePasswordView,
    LoginView,
)

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
]
