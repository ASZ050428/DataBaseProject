from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.ArtistView import ArtistViewSet, ArtistProfileView, UpgradeArtistView

router = DefaultRouter()
router.register(r'', ArtistViewSet, basename='artist')  # 歌手相关接口

urlpatterns = [
    path('profile/', ArtistProfileView.as_view(), name='artist-profile'),
    path('upgrade-artist/', UpgradeArtistView.as_view(), name='artist-upgrade-artist'),
] + router.urls