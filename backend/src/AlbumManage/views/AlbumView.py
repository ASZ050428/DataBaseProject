from rest_framework import viewsets, filters, serializers
from AlbumManage.models import Album
from common.views import BaseReadOnlyViewSet

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class AlbumViewSet(BaseReadOnlyViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=album_name']
