from rest_framework import viewsets, filters, serializers
from CollectionManage.models import CollectionList, CollectionListSongInclude, UserAlbumCollect, UserSingerFollow, SingerSongPublish
from common.views import BaseReadOnlyViewSet

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
