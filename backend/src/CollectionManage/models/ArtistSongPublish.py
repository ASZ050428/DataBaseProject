from django.db import models
from ArtistManage.models import Artist as Singer
from SongManage.models import Song

class SingerSongPublish(models.Model):
    singer_id = models.ForeignKey(
        Singer, 
        on_delete=models.CASCADE, 
        db_column="singer_id",
        verbose_name="歌手ID"
    )
    song_id = models.ForeignKey(
        Song, 
        on_delete=models.CASCADE, 
        db_column="song_id",
        verbose_name="歌曲ID"
    )

    class Meta:
        db_table = "singer_song_publish"
        verbose_name = "歌手歌曲发布"
        verbose_name_plural = "歌手歌曲发布"
        unique_together = ("singer_id", "song_id")  # 组合主键