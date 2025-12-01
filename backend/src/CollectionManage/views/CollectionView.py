from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from CollectionManage.models import CollectionList, CollectionListSongInclude, UserAlbumCollect, UserSingerFollow, SingerSongPublish
from SongManage.models import Song
from AlbumManage.models import Album
from ArtistManage.models.Aritist import Artist
from common.views import BaseReadOnlyViewSet
from utils.response import api_response

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
    queryset = SingerSongPublish.objects.all()
    serializer_class = SingerSongPublishSerializer


class MyCollectionListsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        lists = CollectionList.objects.filter(user_id=request.user).order_by('-create_time')
        data = [{'id': i.list_id, 'title': i.list_name} for i in lists]
        return api_response(data=data)
    def post(self, request):
        name = request.data.get('name') or request.data.get('list_name')
        if not name:
            return api_response(code=1, message='缺少列表名称', data=None)
        obj = CollectionList.objects.create(list_name=name, user_id=request.user)
        return api_response(message='创建成功', data={'id': obj.list_id, 'title': obj.list_name})


class MyCollectionListDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, list_id: int):
        qs = CollectionList.objects.filter(list_id=list_id, user_id=request.user)
        if not qs.exists():
            return api_response(code=2, message='未找到列表', data=None)
        qs.delete()
        return api_response(message='删除成功', data=None)
    def patch(self, request, list_id: int):
        qs = CollectionList.objects.filter(list_id=list_id, user_id=request.user).first()
        if not qs:
            return api_response(code=2, message='未找到列表', data=None)
        name = request.data.get('name') or request.data.get('list_name')
        if not name:
            return api_response(code=1, message='缺少列表名称', data=None)
        qs.list_name = name
        qs.save()
        return api_response(message='重命名成功', data={'id': qs.list_id, 'title': qs.list_name})


class MyCollectionListSongsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, list_id: int):
        lst = CollectionList.objects.filter(list_id=list_id, user_id=request.user).first()
        if not lst:
            return api_response(code=2, message='未找到列表', data=None)
        includes = CollectionListSongInclude.objects.filter(list_id=lst)
        data = [{'id': s.song_id_id, 'title': s.song_id.title} for s in includes.select_related('song_id')]
        return api_response(data=data)
    def post(self, request, list_id: int):
        lst = CollectionList.objects.filter(list_id=list_id, user_id=request.user).first()
        if not lst:
            return api_response(code=2, message='未找到列表', data=None)
        song_id = request.data.get('song_id')
        if not song_id:
            return api_response(code=1, message='缺少歌曲ID', data=None)
        song = Song.objects.filter(pk=song_id).first()
        if not song:
            return api_response(code=3, message='未找到歌曲', data=None)
        obj, created = CollectionListSongInclude.objects.get_or_create(list_id=lst, song_id=song)
        return api_response(message='添加成功', data={'id': song.pk, 'title': song.title})


class MyCollectionListSongDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, list_id: int, song_id: int):
        lst = CollectionList.objects.filter(list_id=list_id, user_id=request.user).first()
        if not lst:
            return api_response(code=2, message='未找到列表', data=None)
        inc = CollectionListSongInclude.objects.filter(list_id=lst, song_id_id=song_id)
        if not inc.exists():
            return api_response(code=3, message='未找到歌曲', data=None)
        inc.delete()
        return api_response(message='删除成功', data=None)


class MyAlbumCollectView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        rows = UserAlbumCollect.objects.filter(user_id=request.user)
        data = [{'id': r.album_id_id, 'title': r.album_id.album_name} for r in rows.select_related('album_id')]
        return api_response(data=data)
    def post(self, request):
        album_id = request.data.get('album_id')
        if not album_id:
            return api_response(code=1, message='缺少专辑ID', data=None)
        album = Album.objects.filter(pk=album_id).first()
        if not album:
            return api_response(code=2, message='未找到专辑', data=None)
        obj, created = UserAlbumCollect.objects.get_or_create(user_id=request.user, album_id=album)
        return api_response(message='收藏成功', data={'id': album.pk, 'title': album.album_name})


class MyAlbumCollectDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, album_id: int):
        qs = UserAlbumCollect.objects.filter(user_id=request.user, album_id_id=album_id)
        if not qs.exists():
            return api_response(code=2, message='未找到收藏', data=None)
        qs.delete()
        return api_response(message='删除成功', data=None)


class MySingerFollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        rows = UserSingerFollow.objects.filter(user_id=request.user)
        data = [{'id': r.singer_id_id, 'title': r.singer_id.name} for r in rows.select_related('singer_id')]
        return api_response(data=data)
    def post(self, request):
        singer_id = request.data.get('singer_id')
        if not singer_id:
            return api_response(code=1, message='缺少歌手ID', data=None)
        singer = Artist.objects.filter(pk=singer_id).first()
        if not singer:
            return api_response(code=2, message='未找到歌手', data=None)
        obj, created = UserSingerFollow.objects.get_or_create(user_id=request.user, singer_id=singer)
        return api_response(message='关注成功', data={'id': singer.pk, 'title': singer.name})


class MySingerFollowDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, singer_id: int):
        qs = UserSingerFollow.objects.filter(user_id=request.user, singer_id_id=singer_id)
        if not qs.exists():
            return api_response(code=2, message='未找到关注', data=None)
        qs.delete()
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
        singer = Artist.objects.filter(pk=singer_id).first()
        song = Song.objects.filter(pk=song_id).first()
        if not singer or not song:
            return api_response(code=3, message='歌手或歌曲不存在', data=None)
        obj, created = SingerSongPublish.objects.get_or_create(singer_id=singer, song_id=song)
        return api_response(message='发布关系创建成功', data={'singer_id': singer.pk, 'song_id': song.pk})
