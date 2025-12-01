from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.UserView import UserViewSet, CustomTokenObtainPairView, RegisterView

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='auth-login'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
]
