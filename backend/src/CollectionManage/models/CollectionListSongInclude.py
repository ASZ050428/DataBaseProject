from django.db import models
from django.utils import timezone
from CollectionManage.models import CollectionList
from SongManage.models import Song

class CollectionListSongInclude(models.Model):
    list_id = models.ForeignKey(
        CollectionList, 
        on_delete=models.CASCADE, 
        db_column="LIST_ID",
        verbose_name="表ID"
    )
    song_id = models.ForeignKey(
        Song, 
        on_delete=models.CASCADE, 
        db_column="SONG_ID",
        verbose_name="歌曲ID"
    )
    add_time = models.DateTimeField(default=timezone.now, db_column="ADD_TIME", verbose_name="收入时间")

    class Meta:
        db_table = "user_song_list_relation"
        verbose_name = "收藏列表歌曲"
        verbose_name_plural = "收藏列表歌曲"
        unique_together = ("list_id", "song_id")  # 组合主键
