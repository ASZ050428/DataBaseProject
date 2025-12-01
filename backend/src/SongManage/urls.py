from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.SongView import SongViewSet

router = DefaultRouter()
router.register(r'', SongViewSet, basename='song')

urlpatterns = [
    path('', include(router.urls)),
]
