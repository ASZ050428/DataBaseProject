from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from SongManage.models import Song
from common.views import BaseReadOnlyViewSet
from utils.response import api_response
from ArtistManage.models.Aritist import Artist
from AlbumManage.models import Album
from django.utils.dateparse import parse_date
from django.db import connection

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class SongViewSet(BaseReadOnlyViewSet):
    queryset = Song.objects.none()
    serializer_class = SongSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=title']
    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search')
        sql = (
            "SELECT song_id, title, artist_id, album_id, duration, release_date, play_count, audio_url, cover_url, create_time, update_time "
            "FROM song"
        )
        params = []
        if search:
            sql += " WHERE title LIKE %s"
            params.append(f"%{search}%")
        sql += " ORDER BY release_date DESC"
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        data = [
            {
                'song_id': r[0],
                'title': r[1],
                'artist': r[2],
                'album_id': r[3],
                'duration': r[4],
                'release_date': r[5],
                'play_count': r[6],
                'audio_url': r[7],
                'cover_url': r[8],
                'create_time': r[9],
                'update_time': r[10],
            }
            for r in rows
        ]
        return api_response(data=data)
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT song_id, title, artist_id, album_id, duration, release_date, play_count, audio_url, cover_url, create_time, update_time FROM song WHERE song_id=%s",
                [pk],
            )
            r = cursor.fetchone()
        if not r:
            return api_response(code=2, message='未找到歌曲', data=None)
        data = {
            'song_id': r[0],
            'title': r[1],
            'artist': r[2],
            'album_id': r[3],
            'duration': r[4],
            'release_date': r[5],
            'play_count': r[6],
            'audio_url': r[7],
            'cover_url': r[8],
            'create_time': r[9],
            'update_time': r[10],
        }
        return api_response(data=data)


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
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM artist WHERE artist_id=%s", [artist_id])
            arow = cursor.fetchone()
        if not arow:
            return api_response(code=3, message='歌手不存在', data=None)
        date = parse_date(release_date)
        if not date:
            return api_response(code=4, message='日期格式错误', data=None)
        if album_id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM album WHERE album_id=%s", [album_id])
                albrow = cursor.fetchone()
            if not albrow:
                return api_response(code=5, message='专辑不存在', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO song (title, artist_id, album_id, duration, release_date, audio_url, cover_url, play_count, create_time, update_time) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                [title, artist_id, album_id, int(duration), str(date), audio_url, cover_url, 0],
            )
            new_id = cursor.lastrowid
            if not new_id:
                cursor.execute(
                    "SELECT song_id FROM song WHERE title=%s AND artist_id=%s ORDER BY song_id DESC LIMIT 1",
                    [title, artist_id],
                )
                r = cursor.fetchone()
                new_id = r[0] if r else None
        return api_response(message='创建成功', data={'id': new_id, 'title': title})
