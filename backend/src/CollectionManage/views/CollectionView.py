from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from CollectionManage.models import CollectionList, CollectionListSongInclude, UserAlbumCollect, UserSingerFollow, SingerSongPublish
from SongManage.models import Song
from AlbumManage.models import Album
from ArtistManage.models.Aritist import Artist
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

class UserSingerFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSingerFollow
        fields = '__all__'

class UserSingerFollowViewSet(BaseReadOnlyViewSet):
    queryset = UserSingerFollow.objects.all()
    serializer_class = UserSingerFollowSerializer

class SingerSongPublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingerSongPublish
        fields = '__all__'

class SingerSongPublishViewSet(BaseReadOnlyViewSet):
    queryset = SingerSongPublish.objects.none()
    serializer_class = SingerSongPublishSerializer
    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search')
        singer_id = request.query_params.get('singer_id')
        song_id = request.query_params.get('song_id')
        where = []
        params = []
        if singer_id:
            where.append("p.singer_id=%s")
            params.append(singer_id)
        if song_id:
            where.append("p.song_id=%s")
            params.append(song_id)
        if search:
            where.append("(s.name LIKE %s OR g.title LIKE %s)")
            like = f"%{search}%"
            params.extend([like, like])
        sql = (
            "SELECT p.singer_id, s.name, p.song_id, g.title FROM singer_song_publish p "
            "JOIN artist s ON p.singer_id=s.artist_id "
            "JOIN song g ON p.song_id=g.song_id "
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
        pk = kwargs.get('pk')
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT p.id, p.singer_id, s.name, p.song_id, g.title FROM singer_song_publish p "
                "JOIN artist s ON p.singer_id=s.artist_id "
                "JOIN song g ON p.song_id=g.song_id WHERE p.id=%s",
                [pk],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到发布关系', data=None)
        data = { 'id': row[0], 'singer_id': row[1], 'singer_name': row[2], 'song_id': row[3], 'song_title': row[4] }
        return api_response(data=data)


class MyCollectionListsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT list_id, list_name FROM collection_list WHERE user_id=%s ORDER BY create_time DESC",
                [request.user.id],
            )
            rows = cursor.fetchall()
        data = [{'id': r[0], 'title': r[1]} for r in rows]
        return api_response(data=data)
    def post(self, request):
        name = request.data.get('name') or request.data.get('list_name')
        if not name:
            return api_response(code=1, message='缺少列表名称', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO collection_list (list_name, user_id, create_time) VALUES (%s, %s, CURRENT_TIMESTAMP)",
                [name, request.user.id],
            )
            new_id = cursor.lastrowid
            if not new_id:
                cursor.execute(
                    "SELECT list_id FROM collection_list WHERE user_id=%s AND list_name=%s ORDER BY create_time DESC LIMIT 1",
                    [request.user.id, name],
                )
                row = cursor.fetchone()
                new_id = row[0] if row else None
        return api_response(message='创建成功', data={'id': new_id, 'title': name})


class MyCollectionListDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, list_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM collection_list WHERE list_id=%s AND user_id=%s",
                [list_id, request.user.id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到列表', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM collection_list WHERE list_id=%s AND user_id=%s",
                [list_id, request.user.id],
            )
        return api_response(message='删除成功', data=None)
    def patch(self, request, list_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM collection_list WHERE list_id=%s AND user_id=%s",
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
                "UPDATE collection_list SET list_name=%s WHERE list_id=%s AND user_id=%s",
                [name, list_id, request.user.id],
            )
        return api_response(message='重命名成功', data={'id': list_id, 'title': name})


class MyCollectionListSongsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, list_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM collection_list WHERE list_id=%s AND user_id=%s",
                [list_id, request.user.id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到列表', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT s.song_id, s.title FROM collection_list_song_include i JOIN song s ON i.song_id=s.song_id WHERE i.list_id=%s ORDER BY i.include_time DESC",
                [list_id],
            )
            rows = cursor.fetchall()
        data = [{'id': r[0], 'title': r[1]} for r in rows]
        return api_response(data=data)
    def post(self, request, list_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM collection_list WHERE list_id=%s AND user_id=%s",
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
                    "INSERT INTO collection_list_song_include (list_id, song_id, include_time) VALUES (%s, %s, CURRENT_TIMESTAMP)",
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
                "SELECT 1 FROM collection_list WHERE list_id=%s AND user_id=%s",
                [list_id, request.user.id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到列表', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM collection_list_song_include WHERE list_id=%s AND song_id=%s",
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
                "SELECT a.album_id, a.album_name FROM user_album_collect u JOIN album a ON u.album_id=a.album_id WHERE u.user_id=%s ORDER BY u.collect_time DESC",
                [request.user.id],
            )
            rows = cursor.fetchall()
        data = [{'id': r[0], 'title': r[1]} for r in rows]
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
                    "INSERT INTO user_album_collect (user_id, album_id, collect_time) VALUES (%s, %s, CURRENT_TIMESTAMP)",
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
                "DELETE FROM user_album_collect WHERE user_id=%s AND album_id=%s",
                [request.user.id, album_id],
            )
            affected = cursor.rowcount
        if affected == 0:
            return api_response(code=2, message='未找到收藏', data=None)
        return api_response(message='删除成功', data=None)


class MySingerFollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT s.artist_id, s.name FROM user_singer_follow u JOIN artist s ON u.singer_id=s.artist_id WHERE u.user_id=%s ORDER BY u.follow_time DESC",
                [request.user.id],
            )
            rows = cursor.fetchall()
        data = [{'id': r[0], 'title': r[1]} for r in rows]
        return api_response(data=data)
    def post(self, request):
        singer_id = request.data.get('singer_id')
        if not singer_id:
            return api_response(code=1, message='缺少歌手ID', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT artist_id, name FROM artist WHERE artist_id=%s",
                [singer_id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到歌手', data=None)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO user_singer_follow (user_id, singer_id, follow_time) VALUES (%s, %s, CURRENT_TIMESTAMP)",
                    [request.user.id, singer_id],
                )
        except IntegrityError:
            pass
        return api_response(message='关注成功', data={'id': int(singer_id), 'title': row[1]})


class MySingerFollowDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, singer_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM user_singer_follow WHERE user_id=%s AND singer_id=%s",
                [request.user.id, singer_id],
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
        singer_id = request.data.get('singer_id')
        song_id = request.data.get('song_id')
        if not singer_id or not song_id:
            return api_response(code=2, message='缺少参数', data=None)
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM artist WHERE artist_id=%s", [singer_id])
            srow = cursor.fetchone()
            cursor.execute("SELECT title FROM song WHERE song_id=%s", [song_id])
            grow = cursor.fetchone()
        if not srow or not grow:
            return api_response(code=3, message='歌手或歌曲不存在', data=None)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO singer_song_publish (singer_id, song_id) VALUES (%s, %s)",
                    [singer_id, song_id],
                )
        except IntegrityError:
            pass
        return api_response(message='发布关系创建成功', data={'singer_id': int(singer_id), 'song_id': int(song_id), 'song_title': grow[0]})

    def delete(self, request):
        role = getattr(getattr(request.user, 'profile', None), 'roles', '')
        if role != 'artist':
            return api_response(code=1, message='仅歌手可取消发布', data=None)
        singer_id = request.data.get('singer_id') or request.query_params.get('singer_id')
        song_id = request.data.get('song_id') or request.query_params.get('song_id')
        if not singer_id or not song_id:
            return api_response(code=2, message='缺少参数', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM singer_song_publish WHERE singer_id=%s AND song_id=%s",
                [singer_id, song_id],
            )
            affected = cursor.rowcount
        if affected == 0:
            return api_response(code=3, message='未找到发布关系', data=None)
        return api_response(message='取消发布成功', data={'singer_id': int(singer_id), 'song_id': int(song_id)})
