from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from AlbumManage.models import Album
from common.views import BaseReadOnlyViewSet
from utils.response import api_response
from ArtistManage.models.Artist import Artist
from django.utils.dateparse import parse_date
from django.db import connection

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
        sql = "SELECT album_id, album_name, release_time, album_artist_id FROM album"
        params = []
        if search:
            sql += " WHERE album_name LIKE %s"
            params.append(f"%{search}%")
        sql += " ORDER BY release_time DESC"
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        data = [{ 'album_id': r[0], 'album_name': r[1], 'release_time': r[2], 'singer_id': r[3] } for r in rows]
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
                "SELECT song_id, title, duration, play_count, audio_url FROM song WHERE album_id=%s ORDER BY song_id ASC",
                [pk]
            )
            songs = [
                {
                    'song_id': r[0],
                    'title': r[1],
                    'duration': r[2],
                    'play_count': r[3],
                    'audio_url': r[4]
                }
                for r in cursor.fetchall()
            ]

        data = {
            **album_info,
            'songs': songs
        }
        return api_response(data=data)


class MyAlbumListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM user_become_artist WHERE user_id=%s", [request.user.id])
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
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        # 仅允许 artist 角色创建
        role = getattr(getattr(request.user, 'profile', None), 'roles', '')
        if role != 'artist':
            # Check SQL too
            is_artist = False
            with connection.cursor() as cursor:
                 cursor.execute("SELECT 1 FROM user_become_artist WHERE user_id=%s", [request.user.id])
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
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk):
        # 验证歌手身份
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM user_become_artist WHERE user_id=%s", [request.user.id])
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
            
            # 删除专辑前，需要把里面的歌曲 album_id 置空? 还是级联删除?
            # 通常应该把歌曲移出专辑，而不是删除歌曲
            cursor.execute("UPDATE song SET album_id=NULL WHERE album_id=%s", [pk])
            
            # 删除专辑
            cursor.execute("DELETE FROM album WHERE album_id=%s", [pk])
            
        return api_response(message='删除成功', data=None)
