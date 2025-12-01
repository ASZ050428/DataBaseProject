from django.db import models
from CollectionManage.models import CollectionList
from SongManage.models import Song

class CollectionListSongInclude(models.Model):
    list_id = models.ForeignKey(
        CollectionList, 
        on_delete=models.CASCADE, 
        db_column="list_id",
        verbose_name="表ID"
    )
    song_id = models.ForeignKey(
        Song, 
        on_delete=models.CASCADE, 
        db_column="song_id",
        verbose_name="歌曲ID"
    )
    include_time = models.DateTimeField(auto_now_add=True, verbose_name="收入时间")

    class Meta:
        db_table = "collection_list_song_include"
        verbose_name = "收藏列表歌曲"
        verbose_name_plural = "收藏列表歌曲"
        unique_together = ("list_id", "song_id")  # 组合主键