from rest_framework.views import APIView
from utils.response import api_response
from utils.jwt_required import jwt_required
from django.db import connection, IntegrityError

class MyCollectionListsView(APIView):

    # 获取我的收藏列表
    @jwt_required
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT cl.LIST_ID, cl.LIST_NAME, cl.CREATE_TIME FROM user_favourite_songs_list cl "
                    "JOIN user_list_relation ulr ON cl.LIST_ID=ulr.LIST_ID "
                    "WHERE ulr.USER_ID=%s ORDER BY cl.CREATE_TIME DESC",
                    [request.user_id],
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

    # 创建新的收藏列表
    @jwt_required
    def post(self, request):
        try:
            name = request.data.get('name') or request.data.get('list_name')
            if not name:
                return api_response(code=1, message='缺少列表名称', data=None)
            # 插入新的收藏列表
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
            # 关联用户和新创建的列表
            if new_id:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO user_list_relation (USER_ID, LIST_ID) VALUES (%s, %s)",
                        [request.user_id, new_id],
                    )
            return api_response(message='创建成功', data={'id': new_id, 'title': name})
        except Exception as e:
            return api_response(code=500, message=f'数据库连接失败: {str(e)}', data=None, status_code=500)


class MyCollectionListDeleteView(APIView):

    # 删除我的收藏列表
    @jwt_required
    def delete(self, request, list_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM user_list_relation WHERE LIST_ID=%s AND USER_ID=%s",
                [list_id, request.user_id],
            )
            row = cursor.fetchone()
        if not row:
            return api_response(code=2, message='未找到列表', data=None)
        with connection.cursor() as cursor:
            # 此处添加了触发器，会自动删除关联数据
            cursor.execute("DELETE FROM user_favourite_songs_list WHERE LIST_ID=%s", [list_id])
        return api_response(message='删除成功', data=None)


class MyCollectionListSongsView(APIView):

    # 获取收藏列表中的歌曲
    @jwt_required
    def get(self, request, list_id: int):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM user_list_relation WHERE LIST_ID=%s AND USER_ID=%s",
                    [list_id, request.user_id],
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
        except Exception as e:
            return api_response(code=500, message=f'数据库连接失败: {str(e)}', data=None, status_code=500)
        
    # 向收藏列表中添加歌曲
    @jwt_required
    def post(self, request, list_id: int):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM user_list_relation WHERE LIST_ID=%s AND USER_ID=%s",
                    [list_id, request.user_id],
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
        except Exception as e:
            return api_response(code=500, message=f'数据库连接失败: {str(e)}', data=None, status_code=500)


class MyCollectionListSongDeleteView(APIView):

    # 从收藏列表中删除歌曲
    @jwt_required
    def delete(self, request, list_id: int, song_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM user_list_relation WHERE LIST_ID=%s AND USER_ID=%s",
                [list_id, request.user_id],
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

    # 获取我收藏的专辑
    @jwt_required
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT a.album_id, a.album_name, u.COLLECT_TIME FROM user_favourite_albums u JOIN album a ON u.ALBUM_ID=a.album_id WHERE u.USER_ID=%s ORDER BY u.COLLECT_TIME DESC",
                [request.user_id],
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
    
    # 收藏专辑
    @jwt_required
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
                    [request.user_id, album_id],
                )
        except IntegrityError:
            pass
        return api_response(message='收藏成功', data={'id': int(album_id), 'title': row[1]})


class MyAlbumCollectDeleteView(APIView):

    # 取消收藏专辑
    @jwt_required
    def delete(self, request, album_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM user_favourite_albums WHERE USER_ID=%s AND ALBUM_ID=%s",
                [request.user_id, album_id],
            )
            affected = cursor.rowcount
        if affected == 0:
            return api_response(code=2, message='未找到收藏', data=None)
        return api_response(message='删除成功', data=None)


class MyArtistFollowView(APIView):

    # 获取我关注的歌手
    @jwt_required
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT s.artist_id, s.artist_name, u.FOLLOW_TIME FROM user_follow_artists u JOIN artist s ON u.ARTIST_ID=s.artist_id WHERE u.USER_ID=%s ORDER BY u.FOLLOW_TIME DESC",
                [request.user_id],
            )
            rows = cursor.fetchall()
        data = [
            {
                'id': r[0], 
                'artist_name': r[1], 
                'follow_time': r[2].strftime('%Y-%m-%d %H:%M:%S') if r[2] else None
            } 
            for r in rows
        ]
        return api_response(data=data)
    
    # 关注歌手
    @jwt_required
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
                    [request.user_id, artist_id],
                )
        except IntegrityError:
            pass
        return api_response(message='关注成功', data={'id': int(artist_id), 'title': row[1]})


class MyArtistFollowDeleteView(APIView):

    # 取消关注歌手
    @jwt_required
    def delete(self, request, artist_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM user_follow_artists WHERE USER_ID=%s AND ARTIST_ID=%s",
                [request.user_id, artist_id],
            )
            affected = cursor.rowcount
        if affected == 0:
            return api_response(code=2, message='未找到关注', data=None)
        return api_response(message='取消成功', data=None)
