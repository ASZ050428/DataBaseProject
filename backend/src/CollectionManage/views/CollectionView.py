from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from CollectionManage.models import CollectionList, CollectionListSongInclude, UserAlbumCollect, UserArtistFollow, ArtistSongPublish
from SongManage.models import Song
from AlbumManage.models import Album
from ArtistManage.models.Artist import Artist
from common.views import BaseReadOnlyViewSet
from utils.response import api_response
from django.db import connection, IntegrityError

class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionList
        fields = '__all__'

class CollectionListViewSet(BaseReadOnlyViewSet):
    queryset = CollectionList.objects.all()
    serializer_class = CollectionListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=list_name']

class CollectionListSongIncludeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionListSongInclude
        fields = '__all__'

class CollectionListSongIncludeViewSet(BaseReadOnlyViewSet):
    queryset = CollectionListSongInclude.objects.all()
    serializer_class = CollectionListSongIncludeSerializer

class UserAlbumCollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAlbumCollect
        fields = '__all__'

class UserAlbumCollectViewSet(BaseReadOnlyViewSet):
    queryset = UserAlbumCollect.objects.all()
    serializer_class = UserAlbumCollectSerializer

class UserArtistFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserArtistFollow
        fields = '__all__'

class UserArtistFollowViewSet(BaseReadOnlyViewSet):
    queryset = UserArtistFollow.objects.all()
    serializer_class = UserArtistFollowSerializer

class ArtistSongPublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistSongPublish
        fields = '__all__'

class ArtistSongPublishViewSet(BaseReadOnlyViewSet):
    queryset = ArtistSongPublish.objects.none()
    serializer_class = ArtistSongPublishSerializer
    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search')
        artist_id = request.query_params.get('artist_id') or request.query_params.get('singer_id')
        song_id = request.query_params.get('song_id')
        where = []
        params = []
        if artist_id:
            where.append("p.ARTIST_ID=%s")
            params.append(artist_id)
        if song_id:
            where.append("p.SONG_ID=%s")
            params.append(song_id)
        if search:
            where.append("(s.artist_name LIKE %s OR g.title LIKE %s)")
            like = f"%{search}%"
            params.extend([like, like])
        sql = (
            "SELECT p.ARTIST_ID, s.artist_name, p.SONG_ID, g.title FROM artist_song_relation p "
            "JOIN artist s ON p.ARTIST_ID=s.artist_id "
            "JOIN song g ON p.SONG_ID=g.song_id "
        )
        if where:
            sql += "WHERE " + " AND ".join(where) + " "
        sql += "ORDER BY g.release_date DESC"
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        data = [
            { 'singer_id': r[0], 'singer_name': r[1], 'song_id': r[2], 'song_title': r[3] }
            for r in rows
        ]
        return api_response(data=data)
    def retrieve(self, request, *args, **kwargs):
        artist_id = kwargs.get('pk')
        song_id = request.query_params.get('song_id')
        if not artist_id or not song_id:
            return api_response(code=1, message='缺少参数', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT p.ARTIST_ID, s.artist_name, p.SONG_ID, g.title FROM artist_song_relation p "
                "JOIN artist s ON p.ARTIST_ID=s.artist_id "
                "JOIN song g ON p.SONG_ID=g.song_id WHERE p.ARTIST_ID=%s AND p.SONG_ID=%s",
                [artist_id, song_id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到发布关系', data=None)
        data = { 'singer_id': row[0], 'singer_name': row[1], 'song_id': row[2], 'song_title': row[3] }
        return api_response(data=data)


class MyCollectionListsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT cl.LIST_ID, cl.LIST_NAME, cl.CREATE_TIME FROM user_favourite_songs_list cl "
                    "JOIN user_list_relation ulr ON cl.LIST_ID=ulr.LIST_ID "
                    "WHERE ulr.USER_ID=%s ORDER BY cl.CREATE_TIME DESC",
                    [request.user.id],
                )
                rows = cursor.fetchall()
            data = [
                {
                    'id': r[0], 
                    'title': r[1],
                    'create_time': r[2].strftime('%Y-%m-%d %H:%M:%S') if r[2] else None
                } 
                for r in rows
            ]
            return api_response(data=data)
        except Exception as e:
            return api_response(code=500, message=f'数据库连接失败: {str(e)}', data=None, status_code=500)
    def post(self, request):
        name = request.data.get('name') or request.data.get('list_name')
        if not name:
            return api_response(code=1, message='缺少列表名称', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO user_favourite_songs_list (LIST_NAME, CREATE_TIME) VALUES (%s, CURRENT_TIMESTAMP)",
                [name],
            )
            new_id = cursor.lastrowid
            if not new_id:
                cursor.execute(
                    "SELECT LIST_ID FROM user_favourite_songs_list WHERE LIST_NAME=%s ORDER BY CREATE_TIME DESC LIMIT 1",
                    [name],
                )
                row = cursor.fetchone()
                new_id = row[0] if row else None
        if new_id:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO user_list_relation (USER_ID, LIST_ID) VALUES (%s, %s)",
                    [request.user.id, new_id],
                )
        return api_response(message='创建成功', data={'id': new_id, 'title': name})


class MyCollectionListDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, list_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM user_list_relation WHERE LIST_ID=%s AND USER_ID=%s",
                [list_id, request.user.id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到列表', data=None)
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM user_song_list_relation WHERE LIST_ID=%s", [list_id])
            cursor.execute("DELETE FROM user_list_relation WHERE LIST_ID=%s AND USER_ID=%s", [list_id, request.user.id])
            cursor.execute("DELETE FROM user_favourite_songs_list WHERE LIST_ID=%s", [list_id])
        return api_response(message='删除成功', data=None)
    def patch(self, request, list_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM user_list_relation WHERE LIST_ID=%s AND USER_ID=%s",
                [list_id, request.user.id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到列表', data=None)
        name = request.data.get('name') or request.data.get('list_name')
        if not name:
            return api_response(code=1, message='缺少列表名称', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE user_favourite_songs_list SET LIST_NAME=%s WHERE LIST_ID=%s",
                [name, list_id],
            )
        return api_response(message='重命名成功', data={'id': list_id, 'title': name})


class MyCollectionListSongsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, list_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM user_list_relation WHERE LIST_ID=%s AND USER_ID=%s",
                [list_id, request.user.id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到列表', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT s.song_id, s.title, s.audio_url, s.duration, s.release_date, a.artist_name, i.ADD_TIME "
                "FROM user_song_list_relation i "
                "JOIN song s ON i.SONG_ID=s.song_id "
                "LEFT JOIN artist a ON s.artist_id=a.artist_id "
                "WHERE i.LIST_ID=%s "
                "ORDER BY i.ADD_TIME DESC",
                [list_id],
            )
            rows = cursor.fetchall()
        data = [
            {
                'song_id': r[0], 
                'title': r[1], 
                'audio_url': r[2],
                'duration': r[3],
                'release_date': r[4],
                'artist_name': r[5],
                'add_time': r[6].strftime('%Y-%m-%d %H:%M:%S') if r[6] else None
            } 
            for r in rows
        ]
        return api_response(data=data)
    def post(self, request, list_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM user_list_relation WHERE LIST_ID=%s AND USER_ID=%s",
                [list_id, request.user.id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到列表', data=None)
        song_id = request.data.get('song_id')
        if not song_id:
            return api_response(code=1, message='缺少歌曲ID', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM song WHERE song_id=%s",
                [song_id],
            )
            srow = cursor.fetchone()
        if not srow:
            return api_response(code=3, message='未找到歌曲', data=None)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO user_song_list_relation (LIST_ID, SONG_ID, ADD_TIME) VALUES (%s, %s, CURRENT_TIMESTAMP)",
                    [list_id, song_id],
                )
        except IntegrityError:
            pass
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT title FROM song WHERE song_id=%s",
                [song_id],
            )
            row = cursor.fetchone()
        return api_response(message='添加成功', data={'id': int(song_id), 'title': row[0] if row else None})


class MyCollectionListSongDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, list_id: int, song_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM user_list_relation WHERE LIST_ID=%s AND USER_ID=%s",
                [list_id, request.user.id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到列表', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM user_song_list_relation WHERE LIST_ID=%s AND SONG_ID=%s",
                [list_id, song_id],
            )
            affected = cursor.rowcount
        if affected == 0:
            return api_response(code=3, message='未找到歌曲', data=None)
        return api_response(message='删除成功', data=None)


class MyAlbumCollectView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT a.album_id, a.album_name, u.COLLECT_TIME FROM user_favourite_albums u JOIN album a ON u.ALBUM_ID=a.album_id WHERE u.USER_ID=%s ORDER BY u.COLLECT_TIME DESC",
                [request.user.id],
            )
            rows = cursor.fetchall()
        data = [
            {
                'id': r[0], 
                'title': r[1], 
                'collect_time': r[2].strftime('%Y-%m-%d %H:%M:%S') if r[2] else None
            } 
            for r in rows
        ]
        return api_response(data=data)
    def post(self, request):
        album_id = request.data.get('album_id')
        if not album_id:
            return api_response(code=1, message='缺少专辑ID', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT album_id, album_name FROM album WHERE album_id=%s",
                [album_id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到专辑', data=None)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO user_favourite_albums (USER_ID, ALBUM_ID, COLLECT_TIME) VALUES (%s, %s, CURRENT_TIMESTAMP)",
                    [request.user.id, album_id],
                )
        except IntegrityError:
            pass
        return api_response(message='收藏成功', data={'id': int(album_id), 'title': row[1]})


class MyAlbumCollectDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, album_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM user_favourite_albums WHERE USER_ID=%s AND ALBUM_ID=%s",
                [request.user.id, album_id],
            )
            affected = cursor.rowcount
        if affected == 0:
            return api_response(code=2, message='未找到收藏', data=None)
        return api_response(message='删除成功', data=None)


class MyArtistFollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT s.artist_id, s.artist_name, u.FOLLOW_TIME FROM user_follow_artists u JOIN artist s ON u.ARTIST_ID=s.artist_id WHERE u.USER_ID=%s ORDER BY u.FOLLOW_TIME DESC",
                [request.user.id],
            )
            rows = cursor.fetchall()
        data = [
            {
                'id': r[0], 
                'title': r[1], 
                'follow_time': r[2].strftime('%Y-%m-%d %H:%M:%S') if r[2] else None
            } 
            for r in rows
        ]
        return api_response(data=data)
    def post(self, request):
        artist_id = request.data.get('artist_id') or request.data.get('singer_id')
        if not artist_id:
            return api_response(code=1, message='缺少歌手ID', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT artist_id, artist_name FROM artist WHERE artist_id=%s",
                [artist_id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到歌手', data=None)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO user_follow_artists (USER_ID, ARTIST_ID, FOLLOW_TIME) VALUES (%s, %s, CURRENT_TIMESTAMP)",
                    [request.user.id, artist_id],
                )
        except IntegrityError:
            pass
        return api_response(message='关注成功', data={'id': int(artist_id), 'title': row[1]})


class MyArtistFollowDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, artist_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM user_follow_artists WHERE USER_ID=%s AND ARTIST_ID=%s",
                [request.user.id, artist_id],
            )
            affected = cursor.rowcount
        if affected == 0:
            return api_response(code=2, message='未找到关注', data=None)
        return api_response(message='取消成功', data=None)


class MyPublishSongLinkView(APIView):
    """创建歌手-歌曲发布关系"""
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        role = getattr(getattr(request.user, 'profile', None), 'roles', '')
        if role != 'artist':
            return api_response(code=1, message='仅歌手可发布', data=None)
        artist_id = request.data.get('artist_id') or request.data.get('singer_id')
        song_id = request.data.get('song_id')
        if not artist_id or not song_id:
            return api_response(code=2, message='缺少参数', data=None)
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM artist WHERE artist_id=%s", [artist_id])
            srow = cursor.fetchone()
            cursor.execute("SELECT title FROM song WHERE song_id=%s", [song_id])
            grow = cursor.fetchone()
        if not srow or not grow:
            return api_response(code=3, message='歌手或歌曲不存在', data=None)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO artist_song_relation (ARTIST_ID, SONG_ID) VALUES (%s, %s)",
                    [artist_id, song_id],
                )
        except IntegrityError:
            pass
        return api_response(message='发布关系创建成功', data={'singer_id': int(artist_id), 'song_id': int(song_id), 'song_title': grow[0]})

    def delete(self, request):
        role = getattr(getattr(request.user, 'profile', None), 'roles', '')
        if role != 'artist':
            return api_response(code=1, message='仅歌手可取消发布', data=None)
        artist_id = request.data.get('artist_id') or request.query_params.get('artist_id') or request.data.get('singer_id') or request.query_params.get('singer_id')
        song_id = request.data.get('song_id') or request.query_params.get('song_id')
        if not artist_id or not song_id:
            return api_response(code=2, message='缺少参数', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM artist_song_relation WHERE ARTIST_ID=%s AND SONG_ID=%s",
                [artist_id, song_id],
            )
            affected = cursor.rowcount
        if affected == 0:
            return api_response(code=3, message='未找到发布关系', data=None)
        return api_response(message='取消发布成功', data={'singer_id': int(artist_id), 'song_id': int(song_id)})
