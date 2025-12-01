from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from AlbumManage.models import Album
from common.views import BaseReadOnlyViewSet
from utils.response import api_response
from ArtistManage.models.Aritist import Artist
from django.utils.dateparse import parse_date

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class AlbumViewSet(BaseReadOnlyViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=album_name']


class MyAlbumCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        # 仅允许 artist 角色创建
        role = getattr(getattr(request.user, 'profile', None), 'roles', '')
        if role != 'artist':
            return api_response(code=1, message='仅歌手可创建专辑', data=None)
        name = request.data.get('album_name')
        release_time = request.data.get('release_time')
        singer_id = request.data.get('singer_id')
        if not name or not release_time or not singer_id:
            return api_response(code=2, message='缺少参数', data=None)
        singer = Artist.objects.filter(pk=singer_id).first()
        if not singer:
            return api_response(code=3, message='歌手不存在', data=None)
        date = parse_date(release_time)
        if not date:
            return api_response(code=4, message='日期格式错误', data=None)
        a = Album.objects.create(album_name=name, release_time=date, singer_id=singer)
        return api_response(message='创建成功', data={'id': a.album_id, 'title': a.album_name})
