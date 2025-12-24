from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from AlbumManage.models import Album
from common.views import BaseReadOnlyViewSet
from utils.response import api_response
from ArtistManage.models.Artist import Artist
from django.utils.dateparse import parse_date
from django.db import connection, transaction, IntegrityError
from utils.jwt_required import jwt_required

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class AlbumViewSet(BaseReadOnlyViewSet):
    queryset = Album.objects.none()
    serializer_class = AlbumSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=album_name']
    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search')
        sql = "SELECT album_id, album_name, release_time, artist_name FROM album JOIN artist ON album.album_artist_id = artist.artist_id"
        params = []
        if search:
            sql += " WHERE album_name LIKE %s"
            params.append(f"%{search}%")
        sql += " ORDER BY release_time DESC"
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        data = [{ 'album_id': r[0], 'album_name': r[1], 'release_time': r[2], 'artist_name': r[3] } for r in rows]
        return api_response(data=data)
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        with connection.cursor() as cursor:
            # 1. 获取专辑基本信息
            cursor.execute(
                "SELECT album_id, album_name, release_time, album_artist_id FROM album WHERE album_id=%s",
                [pk],
            )
            row = cursor.fetchone()
            if not row:
                return api_response(code=2, message='未找到专辑', data=None)
            
            album_info = { 
                'album_id': row[0], 
                'album_name': row[1], 
                'release_time': row[2], 
                'singer_id': row[3] 
            }

            # 2. 获取专辑内的歌曲
            cursor.execute(
                "SELECT song_id, title, duration, audio_url FROM song WHERE album_id=%s ORDER BY song_id ASC",
                [pk]
            )
            songs = [
                {
                    'song_id': r[0],
                    'title': r[1],
                    'duration': r[2],
                    'audio_url': r[3]
                }
                for r in cursor.fetchall()
            ]

            # 3. 获取歌手名称
            cursor.execute(
                "SELECT artist_name FROM artist WHERE artist_id=%s",
                [album_info['singer_id']]
            )
            artist_row = cursor.fetchone()
            artist_name = artist_row[0] if artist_row else ''


        data = {
            **album_info,
            'songs': songs,
            'artist_name': artist_name
        }
        return api_response(data=data)


class MyAlbumListView(APIView):
    @jwt_required
    def get(self, request):
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM user_become_artist WHERE user_id=%s", [request.user_id])
            row = cursor.fetchone()
            if row:
                artist_id = row[0]
        if not artist_id:
             return api_response(code=1, message='仅歌手可查看专辑列表', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT album_id, album_name, release_time, album_artist_id "
                "FROM album WHERE album_artist_id=%s ORDER BY release_time DESC",
                [artist_id]
            )
            rows = cursor.fetchall()
        data = [
            {
                'album_id': r[0],
                'album_name': r[1],
                'release_time': r[2],
                'singer_id': r[3]
            }
            for r in rows
        ]
        return api_response(data=data)

class MyAlbumCreateView(APIView):
    @jwt_required
    def post(self, request):
        is_artist = False
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM user_become_artist WHERE user_id=%s", [request.user_id])
            if cursor.fetchone():
                is_artist = True
        if not is_artist:
            return api_response(code=1, message='仅歌手可创建专辑', data=None)
        name = request.data.get('album_name')
        release_time = request.data.get('release_time')
        singer_id = request.data.get('singer_id')
        if not name or not release_time or not singer_id:
            return api_response(code=2, message='缺少参数', data=None)
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM artist WHERE artist_id=%s", [singer_id])
            srow = cursor.fetchone()
        if not srow:
            return api_response(code=3, message='歌手不存在', data=None)
        date = parse_date(release_time)
        if not date:
            return api_response(code=4, message='日期格式错误', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO album (album_name, release_time, album_artist_id) VALUES (%s, %s, %s)",
                [name, str(date), singer_id],
            )
            new_id = cursor.lastrowid
            if not new_id:
                cursor.execute(
                    "SELECT album_id FROM album WHERE album_name=%s AND album_artist_id=%s ORDER BY album_id DESC LIMIT 1",
                    [name, singer_id],
                )
                r = cursor.fetchone()
                new_id = r[0] if r else None
        return api_response(message='创建成功', data={'id': new_id, 'title': name})

class MyAlbumDeleteView(APIView):
    @jwt_required
    def delete(self, request, pk):
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM user_become_artist WHERE user_id=%s", [request.user_id])
            row = cursor.fetchone()
            if row:
                artist_id = row[0]
        if not artist_id:
            return api_response(code=1, message='仅歌手可操作', data=None)
        with connection.cursor() as cursor:
            cursor.execute("SELECT album_artist_id FROM album WHERE album_id=%s", [pk])
            row = cursor.fetchone()
            if not row:
                return api_response(code=404, message='专辑不存在', data=None)
            if row[0] != artist_id:
                return api_response(code=403, message='无权删除此专辑', data=None)
            try:
                with transaction.atomic():
                    cursor.execute("DELETE FROM user_favourite_albums WHERE ALBUM_ID=%s", [pk])
                    cursor.execute("UPDATE song SET album_id=NULL WHERE album_id=%s", [pk])
                    cursor.execute("DELETE FROM album WHERE album_id=%s", [pk])
            except IntegrityError as e:
                return api_response(code=500, message=f'数据库错误: {str(e)}', data=None)
            except Exception as e:
                return api_response(code=500, message=f'删除失败: {str(e)}', data=None)
        return api_response(message='删除成功', data=None)
