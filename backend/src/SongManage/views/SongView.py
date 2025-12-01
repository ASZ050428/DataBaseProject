from rest_framework import viewsets, filters, serializers
from SongManage.models import Song
from common.views import BaseReadOnlyViewSet

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class SongViewSet(BaseReadOnlyViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=title']
