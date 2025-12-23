"""music_manage_system_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from UserManage.views.UserView import (
    RegisterView,
    MeView,
    ChangePasswordView,
)
from ArtistManage.views.ArtistView import UpgradeArtistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('UserManage.urls')),
    path('api/artist/', include('ArtistManage.urls')),
    path('api/album/', include('AlbumManage.urls')),
    path('api/song/', include('SongManage.urls')),
    path('api/comment/', include('CommentManage.urls')),
    path('api/collection/', include('CollectionManage.urls')),
    path('api/auth/register/', RegisterView.as_view(), name='auth-register-root'),
    path('api/auth/upgrade-artist/', UpgradeArtistView.as_view(), name='auth-upgrade-artist'),
    path('api/auth/me/', MeView.as_view(), name='auth-me'),
    path('api/auth/change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
