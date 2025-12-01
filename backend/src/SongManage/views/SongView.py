from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from SongManage.models import Song
from common.views import BaseReadOnlyViewSet
from utils.response import api_response
from ArtistManage.models.Aritist import Artist
from AlbumManage.models import Album
from django.utils.dateparse import parse_date

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class SongViewSet(BaseReadOnlyViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=title']


class MySongCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        role = getattr(getattr(request.user, 'profile', None), 'roles', '')
        if role != 'artist':
            return api_response(code=1, message='仅歌手可创建歌曲', data=None)
        title = request.data.get('title')
        artist_id = request.data.get('artist_id')
        album_id = request.data.get('album_id')
        duration = request.data.get('duration')
        release_date = request.data.get('release_date')
        audio_url = request.data.get('audio_url')
        cover_url = request.data.get('cover_url')
        if not title or not artist_id or not duration or not release_date or not audio_url:
            return api_response(code=2, message='缺少参数', data=None)
        artist = Artist.objects.filter(pk=artist_id).first()
        if not artist:
            return api_response(code=3, message='歌手不存在', data=None)
        date = parse_date(release_date)
        if not date:
            return api_response(code=4, message='日期格式错误', data=None)
        s = Song.objects.create(
            title=title,
            artist=artist,
            album_id=album_id,
            duration=int(duration),
            release_date=date,
            audio_url=audio_url,
            cover_url=cover_url,
        )
        return api_response(message='创建成功', data={'id': s.song_id, 'title': s.title})
